from rest_framework import routers

from books.views import (
    BookViewSet,
    ReadingListViewSet,
    FavoriteViewSet,
)


router = routers.SimpleRouter()
router.register(r'book', BookViewSet)
router.register(r'reading', ReadingListViewSet)
router.register(r'favourite', FavoriteViewSet)

urlpatterns = router.urls
