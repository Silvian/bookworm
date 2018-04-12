from rest_framework import routers

from meta_info.views import (
    TagViewSet,
    MetaViewSet,
)


router = routers.SimpleRouter()
router.register(r'tag', TagViewSet)
router.register(r'meta', MetaViewSet)

urlpatterns = router.urls
