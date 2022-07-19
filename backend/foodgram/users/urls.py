from rest_framework.routers import DefaultRouter

from django.urls import include, path, re_path

from .views import UsersViewSet


router = DefaultRouter()
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
