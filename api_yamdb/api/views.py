from rest_framework import filters, viewsets

from reviews.models import Genre, Category, Title
from .permissions import IsAdminOrSuperUser
from .serializers import GenreSerializer, CategorySerializer, TitleSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .mixins import CreateListDestroy


class GenreViewSet(CreateListDestroy):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrSuperUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class CategoryViewSet(CreateListDestroy):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrSuperUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrSuperUser]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')

