from rest_framework import routers

from books.views import (
    BookViewSet,
    BookProgressViewSet,
    BookReviewViewSet,
)


router = routers.SimpleRouter()
router.register(r'book', BookViewSet)
router.register(r'progress', BookProgressViewSet)
router.register(r'review', BookReviewViewSet)

urlpatterns = router.urls
