from .views import TitleViewSet
from rest_framework import routers

routers = routers.DefaultRouter
routers.register('titles', TitleViewSet)
