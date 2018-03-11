from rest_framework import (viewsets, filters)

from books.models import (Book, ReadingList)
from books.serializers import (BookSerializer, ReadingListSerializer)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)


class ReadingListViewSet(viewsets.ModelViewSet):
    queryset = ReadingList.objects.all()
    serializer_class = ReadingListSerializer

    def get_queryset(self, request=None, *args, **kwargs):
        queryset = ReadingList.objects.filter(
                user=self.request.user).prefetch_related('book')
        return queryset
