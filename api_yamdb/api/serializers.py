from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Review, Comment, Title, Genre, Category
from rest_framework.relations import SlugRelatedField


class TitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    genre = SlugRelatedField(
        slug_field='name',
        read_only=True,
        many=True,
    )

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('year',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    rating_average = serializers.SerializerMethodField()

    def validate_score(self, value):
        if 0 >= value >= 10:
            raise serializers.ValidationError('Rating from 1 to 10!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (request.method == 'POST' and
                Review.objects.filter(title=title, author=author).exists()):
            raise ValidationError('You can only leave one '
                                  'review for a product!')
        return data

    class Meta:
        fields = '__all__'
        model = Review

    def rating_average(self):
        return Title.objects.aggregate(Avg('score'))


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
