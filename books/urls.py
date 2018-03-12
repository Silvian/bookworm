from rest_framework import routers

from books.views import (BookViewSet, ReadingListViewSet)


router = routers.SimpleRouter()
router.register(r'book', BookViewSet)
router.register(r'reading', ReadingListViewSet)

urlpatterns = router.urls
