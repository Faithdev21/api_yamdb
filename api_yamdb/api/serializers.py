from reviews.models import Title
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
        read_only_fields = ('year', )
