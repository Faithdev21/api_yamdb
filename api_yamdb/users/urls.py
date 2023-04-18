from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, get_confirmation


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/signup/', get_confirmation),
]
