"""Books app views."""

from rest_framework import (viewsets, filters)

from books.models import (
    Book,
    ReadingList,
    Favourite,
)
from books.serializers import (
    BookSerializer,
    ReadingListSerializer,
    FavouriteSerializer,
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)


class ReadingListViewSet(viewsets.ModelViewSet):
    queryset = ReadingList.objects.all()
    serializer_class = ReadingListSerializer

    def get_queryset(self, request=None, *args, **kwargs):
        """Return reading list objects filtered by user and book related."""
        queryset = ReadingList.objects.filter(
                user=self.request.user).prefetch_related('book')
        return queryset


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer

    def get_queryset(self):
        """Return the queryset of favourites for this user."""
        return Favourite.objects.filter(user=self.request.user)
