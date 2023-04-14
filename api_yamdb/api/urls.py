from django.urls import path, include
from .views import GenreViewSet, CategoryViewSet, TitleViewSet
from rest_framework import routers

router_v1 = routers.DefaultRouter()
router_v1.register('genres', GenreViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]

