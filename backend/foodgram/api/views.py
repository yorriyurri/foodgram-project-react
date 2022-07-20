from rest_framework import filters, viewsets


from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer
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
    queryset = Recipe.objects.all()

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
