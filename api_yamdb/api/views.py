from reviews.models import Genre
from .serializers import GenreSerializer
from rest_framework import filters, mixins, viewsets
from rest_framework.viewsets import GenericViewSet


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = 'If SAFE - ALL, else - Admin'
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
