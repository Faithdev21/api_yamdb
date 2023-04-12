from reviews.models import Category
from api_yamdb.api.serializers import CategorySerializer
from rest_framework import filters, mixins, viewsets
from rest_framework.viewsets import GenericViewSet


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = 'If SAFE - ALL, else - Admin'
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
