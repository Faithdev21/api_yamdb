from api import constants
from rest_framework import serializers

from .models import User
from .validators import validate_email_length, validate_username


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields: tuple[str] = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class MeSerializer(serializers.ModelSerializer):
    """Serializer for User model without permission to change role."""
    class Meta:
        model = User
        fields: [str] = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields: tuple[str] = ('role',)


class UserSignupSerializer(serializers.Serializer):
    """Serializer for User signup."""
    username = serializers.CharField(
        required=True,
        max_length=constants.USER_USERNAME_MAX_LENGTH,
        validators=[validate_username, ]
    )
    email = serializers.EmailField(
        required=True,
        validators=[validate_email_length, ]
    )


class TokenSerializer(serializers.Serializer):
    """Serializer for getting token."""
    username = serializers.CharField(
        required=True,
        max_length=constants.USER_USERNAME_MAX_LENGTH,
        validators=[validate_username, ]
    )
    confirmation_code = serializers.CharField(required=True)
