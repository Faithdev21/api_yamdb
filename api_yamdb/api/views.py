from rest_framework import filters, mixins, viewsets
from rest_framework.viewsets import GenericViewSet, TitleViewSet
from reviews.models import Genre, Category, Title
from .serializers import GenreSerializer, CategorySerializer, TitleSerializer



class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = 'If SAFE - ALL, else - Admin'
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)

class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = 'If SAFE - ALL, else - Admin'
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    
    
class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = ('Add later')