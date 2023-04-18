from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, get_confirmation
from .views import UserViewSet, get_token

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('api/v1/', include(router_v1.urls)),
    path('api/v1/auth/signup/', get_confirmation),
    path('api/v1/auth/token/', get_token)
]
