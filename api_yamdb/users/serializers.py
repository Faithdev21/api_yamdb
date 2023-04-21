from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User
from .validators import validate_username, validate_username_length, validate_email_length


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            validate_username,
            validate_username_length,
        ],
        required=True
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            validate_email_length,
        ],
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class MeSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[validate_username, ]
    )
    email = serializers.EmailField(
        required=True,
        validators=[validate_email_length, ]
    )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[validate_username, ]
    )
    confirmation_code = serializers.CharField(required=True)
