from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializer, TokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST', ])
def get_confirmation(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        user, _ = User.objects.get_or_create(email=email, username=username)
        code = default_token_generator.make_token(user)
        send_mail(
            'Confirmation code',
            f'{username}!, your confirmation code is: {code}',
            'from@example.com',
            [email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        username = get_object_or_404(
            User,
            username=serializer.validated_data.get('username')
        )
        code = serializer.validated_data.get('confirmation_code')
        if default_token_generator.check_token(username, code):
            refresh = RefreshToken.for_user(username)
            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(token, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
