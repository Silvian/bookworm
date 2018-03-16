"""Books app views."""

from rest_framework import (viewsets, filters)

from meta_info.models import (
    Tag,
    MetaInfo,
)
from meta_info.serializers import (
    TagSerializer,
    MetaSerializer,
)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('copy',)


class MetaViewSet(viewsets.ModelViewSet):
    queryset = MetaInfo.objects.all()
    serializer_class = MetaSerializer