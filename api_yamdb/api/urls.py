from .views import CategoryViewSet
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers


router = routers.DefaultRouter
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls.jwt')),  # Работа с токенами
]
