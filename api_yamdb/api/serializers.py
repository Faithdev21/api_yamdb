from api import constants
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from users.validators import validate_email_length, validate_username


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre model."""

    class Meta:
        model = Genre
        fields: tuple[str, ...] = ('name', 'slug')
        lookup_field: str = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""

    class Meta:
        model = Category
        fields: tuple[str, ...] = ('name', 'slug')
        lookup_field: str = 'slug'


class TitleWriteSerializer(serializers.ModelSerializer):
    """Serializer for Title model. POST, PATCH methods."""
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )

    class Meta:
        model = Title
        fields: str = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    """Serializer for Title model. Just safe methods."""
    genre = GenreSerializer(many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields: str = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value: int) -> int:
        """Rating validation."""
        if 0 >= value >= 10:
            raise serializers.ValidationError('Rating from 1 to 10!')
        return value

    def validate(self, data: dict) -> dict:
        """Checking the limit on the maximum number of product reviews."""
        request = self.context['request']
        author = request.user
        title_id: int = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (request.method == 'POST' and Review.objects.filter(
                title=title, author=author).exists()):
            raise ValidationError('You can only leave '
                                  'one review for a product!')
        return data

    class Meta:
        fields: str = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields: str = '__all__'
        model = Comment


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
