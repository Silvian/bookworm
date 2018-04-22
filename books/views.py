"""Books app views."""

from rest_framework import (viewsets, filters)

from books.models import (
    Book,
    BookProgress,
    BookReview,
)
from books.serializers import (
    BookSerializer,
    BookProgressSerializer,
    BookReviewSerializer,
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)


class BookProgressViewSet(viewsets.ModelViewSet):
    queryset = BookProgress.objects.all()
    serializer_class = BookProgressSerializer

    def create(self, request, *args, **kwargs):
        # Test for REVIEW data available
        return super().create(request, *args, **kwargs)


class BookReviewViewSet(viewsets.ModelViewSet):
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer

    def create(self, request, *args, **kwargs):
        # Test for progress data available
        return super().create(request, *args, **kwargs)
