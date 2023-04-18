from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, get_token


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/token/', get_token)
]
