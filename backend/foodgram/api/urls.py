from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientsViewSet, RecipeViewSet, TagViewSet


app_name = 'api'

router = DefaultRouter()
# router.register('users', UsersViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientsViewSet)
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
