from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, get_token, get_confirmation


urlpatterns = [
    path('signup/', get_confirmation),
    path('token/', get_token),
]

