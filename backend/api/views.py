from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .paginations import RecipesPagination
from .permissions import IsAdminOrReadOnly, IsAuthorReadOnly
from .serializers import (IngredientSerializer, MinInfoRecipeSerializer,
                          RecipeCreateSerializer, RecipeSerializer,
                          TagSerializer)
from recipes.models import (Favorite, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart, Tag)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [IngredientFilter]
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.order_by('-id')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorReadOnly,)
    pagination_class = RecipesPagination

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateSerializer

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values_list(
            'ingredient__name',
            'ingredient__measurement_unit',
        ).order_by(
            'ingredient__name',
        ).annotate(
            total_amount=Sum('amount')
        )
        shopping_cart = 'Список покупок:\n'
        for number, ingredient in enumerate(ingredients, start=1):
            shopping_cart += (
                f"{number}. {ingredient[0]} - "
                f"{ingredient[2]} "
                f"{ingredient[1]}\n"
            )
        shopping_cart_filename = 'shopping_cart.txt'
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response['Content-Disposition'] = (
            f'attachment; filename={shopping_cart_filename}'
        )
        return response

    def create_or_destroy(self, request, model, id):
        recipe = get_object_or_404(Recipe, id=id)
        model_instance = model.objects.filter(
            user=request.user, recipe__id=recipe.id
        )
        if request.method == 'POST':
            if model_instance.exists():
                return Response(
                    {'errors': 'Рецепт не был добавлен ранее.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            model.objects.create(user=request.user, recipe=recipe)
            serializer = MinInfoRecipeSerializer()
            return Response(serializer.to_representation(instance=recipe),
                            status=status.HTTP_201_CREATED)
        if model_instance.exists():
            model_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Рецепт не был добавлен ранее.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        return self.create_or_destroy(request, Favorite, pk)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        return self.create_or_destroy(request, ShoppingCart, pk)
