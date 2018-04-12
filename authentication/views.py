"""Books app views."""

from rest_framework import (viewsets, filters)

from authentication.models import (
    ContactMethod,
    Profile,
)
from authentication.serializers import (
    ContactMethodSerializer,
    ProfileSerializer,
)


class ContactMethodViewSet(viewsets.ModelViewSet):
    queryset = ContactMethod.objects.all()
    serializer_class = ContactMethodSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('detail',)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name_first',
        'name_last',
        'email',
    )

    def get_queryset(self, request=None, *args, **kwargs):
        """Return reading list objects filtered by user and book related."""
        queryset = Profile.objects.filter(user=self.request.user)
        return queryset
