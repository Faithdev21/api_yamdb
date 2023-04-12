from .views import GenreViewSet
from rest_framework import routers

router = routers.DefaultRouter
router.register('categories', GenreViewSet)
