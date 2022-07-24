from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeSerializer, TagSerializer)
from recipes.models import Ingredient, Recipe, Tag


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.order_by('-id')

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateSerializer

    def for_responses(self, request, obj, id):
        item = obj.objects.filter(user=request.user, recipe__id=id)
        if (request.method == 'POST') and (not item.exists()):
            recipe = get_object_or_404(Recipe, id=id)
            obj.objects.create(user=request.user, recipe=recipe)
            serializer = RecipeCreateSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif (request.method == 'DELETE') and (item.exists()):
            item.delete()
            return Response(
                {'success': 'Рецепт успешно удален.'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {'errors': 'Ошибка валидации.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
