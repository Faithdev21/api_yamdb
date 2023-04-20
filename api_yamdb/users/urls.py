from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, get_token, get_confirmation

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', get_confirmation),
    path('auth/token/', get_token),
    path('', include(router_v1.urls)),
]

