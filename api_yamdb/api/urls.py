from django.contrib import admin
from django.urls import path, include
from .views import GenreViewSet, CategoryViewSet, TitleViewSet
from rest_framework import routers

router = routers.DefaultRouter
router.register('categories', GenreViewSet)
router.register('categories', CategoryViewSet)
routers.register('titles', TitleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls.jwt')),  # Работа с токенами
]

