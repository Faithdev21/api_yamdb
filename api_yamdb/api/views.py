from api.permissions import IsAdmin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User

from .filters import TitlesFilter
from .mixins import CreateListDestroy
from .permissions import AdminModeratorAuthorPermission, IsAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, MeSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          TokenSerializer, UserSerializer,
                          UserSignupSerializer)


class GenreViewSet(CreateListDestroy):
    """Viewset for instances of the genre of the title class."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'
    pagination_class = PageNumberPagination


class CategoryViewSet(CreateListDestroy):
    """Viewset for instances of the category of the title class."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields: tuple[str] = ('name',)
    lookup_field: str = 'slug'
    pagination_class = PageNumberPagination


class TitleViewSet(viewsets.ModelViewSet):
    """Viewset for instances of the title class."""
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleReadSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleWriteSerializer
        return TitleReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Viewset for instances of the review of the title class."""
    serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        title = get_object_or_404(
            Title.objects.annotate(rating=Avg('reviews__score')),
            pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset for instances of the comment to review class."""
    serializer_class = CommentSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


@api_view(['POST', ])
@permission_classes([AllowAny])
def get_confirmation(request):
    """User registration with confirmation code sent to email address."""
    serializer = UserSignupSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        try:
            username: str = serializer.validated_data.get('username')
            email: str = serializer.validated_data.get('email')
            user, _ = User.objects.get_or_create(
                email=email, username=username)
        except IntegrityError:
            error: str = (
                'login failed'
                if User.objects.filter(username=username).exists()
                else 'email already exists'
            )
            return Response(error, status.HTTP_400_BAD_REQUEST)
        confirmation_code: str = default_token_generator.make_token(user)
        send_mail(
            'Confirmation code',
            f'{username}!, your confirmation code is: {confirmation_code}',
            'from@example.com',
            [email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_classes([AllowAny])
def get_token(request):
    """Checking the confirmation code and issuing a token."""
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        username = get_object_or_404(
            User,
            username=serializer.validated_data.get('username')
        )
        code: str = serializer.validated_data.get('confirmation_code')
        if default_token_generator.check_token(username, code):
            refresh = RefreshToken.for_user(username)
            token: dict[str, str] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(token, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Viewset for instances of the user class."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field: str = 'username'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields: list[str] = ['=username']
    http_method_names: list[str] = ['get', 'post', 'patch', 'delete']

    @action(detail=False,
            url_path='me', url_name='me',
            methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def user_profile(self, request):
        serializer = MeSerializer(self.request.user)
        if request.method == 'PATCH':
            serializer = MeSerializer(
                self.request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role, partial=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)
