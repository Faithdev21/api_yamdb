from reviews.models import Title, Genre, Category
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


class TitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    genre = SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('year',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
        read_only_fields = ('slug',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('slug',)
