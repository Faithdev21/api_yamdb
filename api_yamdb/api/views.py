
from rest_framework import filters, mixins, viewsets
from rest_framework.viewsets import GenericViewSet
from reviews.models import Genre, Category
from .serializers import GenreSerializer, CategorySerializer



class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = 'If SAFE - ALL, else - Admin'
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
