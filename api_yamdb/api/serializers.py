from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre model."""

    class Meta:
        model = Genre
        fields: tuple[str, str] = ('name', 'slug')
        lookup_field: str = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""

    class Meta:
        model = Category
        fields: tuple[str, str] = ('name', 'slug')
        lookup_field: str = 'slug'


class TitlePostSerializer(serializers.ModelSerializer):
    """Serializer for Title model for not safe methods."""
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


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for Title model for safe methods."""
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
        """Checks the rating requirements."""
        if 0 >= value >= 10:
            raise serializers.ValidationError('Rating from 1 to 10!')
        return value

    def validate(self, data: dict) -> dict:
        """Checks the limits on the maximum number of reviews per product."""
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
