from api.permissions import IsAdmin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (MeSerializer, TokenSerializer, UserSerializer,
                          UserSignupSerializer)


@api_view(['POST', ])
@permission_classes([AllowAny])
def get_confirmation(request):
    """Registers the user
    and sends him a confirmation code to the email address."""
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
    """Checks the confirmation code and issues a token."""
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
    """Provides views for instances of the user class."""
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
