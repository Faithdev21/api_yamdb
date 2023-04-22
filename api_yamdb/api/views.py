from django.db.models import Avg
from rest_framework import filters, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination

from reviews.models import Genre, Category, Title, Review
from .filters import TitlesFilter
from .permissions import AdminModeratorAuthorPermission, IsAdminOrReadOnly
from .serializers import GenreSerializer, CategorySerializer, TitleSerializer, ReviewSerializer, CommentSerializer, \
    TitlePostSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .mixins import CreateListDestroy


class GenreViewSet(CreateListDestroy):
    """Provides views for instances of the genre of the title class."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'
    pagination_class = PageNumberPagination


class CategoryViewSet(CreateListDestroy):
    """Provides views for instances of the category of the title class."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'
    pagination_class = PageNumberPagination


class TitleViewSet(viewsets.ModelViewSet):
    """Provides views for instances of the title class."""
    queryset = Title.objects.annotate(rating=Avg("reviews__score"))
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.request.method == ('POST' or 'PATCH'):
            return TitlePostSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Provides views for instances of the review of the title class."""
    serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        title = get_object_or_404(
            Title.objects.annotate(rating=Avg('reviews__score')),
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Provides views for instances of the comment to review class."""
    serializer_class = CommentSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
