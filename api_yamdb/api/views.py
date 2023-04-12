from reviews.models import Title
from .serializers import TitleSerializer
from rest_framework import filters, mixins, viewsets


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = ('Add later')