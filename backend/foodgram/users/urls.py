from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import UsersViewSet


router = DefaultRouter()
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path("", include(router.urls)),
]