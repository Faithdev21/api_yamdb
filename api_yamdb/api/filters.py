from django_filters.rest_framework import CharFilter, FilterSet

from reviews.models import Title


class TitlesFilter(FilterSet):
    name = CharFilter(field_name="name")
    category = CharFilter(field_name="category__slug")
    genre = CharFilter(field_name="genre__slug", lookup_expr="contains")

    class Meta:
        model = Title
        fields = '__all__'
