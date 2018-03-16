from rest_framework import routers

from profile.views import (
    ProfileViewSet,
    ContactMethodViewSet,
)


router = routers.SimpleRouter()
router.register(r'profile', ProfileViewSet)
router.register(r'contacts', ContactMethodViewSet)

urlpatterns = router.urls
