"""Books app serializers."""

from rest_framework import serializers

from meta_info.serializers import MetaSerializer

from books.exceptions import OperationReservedInternally
from books.models import (
    Book,
    BookProgress,
    BookReview,
)


class ProfileAssociationSerializerMixin:
    """Manage the creation of an object with reference to a Profile."""

    def validate(self, data):
        """Validate for profile assignment to validated_data"""
        current_user = self.context['request'].user
        if 'profile' not in data:
            data['profile'] = current_user.profile
        elif current_user.id != data['profile']:
            if not current_user.is_superuser and not current_user.is_staff:
                raise OperationReservedInternally(current_user)
        return super().validate(data)


class BookSerializer(MetaSerializer, ProfileAssociationSerializerMixin):
    class Meta:
        model = Book
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
        )
        fields = read_only_fields + (
            'title',
            'description',
            'reviews',
            'meta',
        )
        exclude = []


class BookProgressSerializer(
        serializers.ModelSerializer, ProfileAssociationSerializerMixin):
    book = BookSerializer()

    class Meta:
        model = BookProgress
        exclude = []
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
        )
        fields = read_only_fields + (
            'percent',
            'page',
            'progress',
            'book',
        )


class BookReviewSerializer(MetaSerializer, ProfileAssociationSerializerMixin):
    book = BookSerializer()
    progress = BookProgressSerializer()

    class Meta:
        model = BookReview
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
        )
        fields = read_only_fields + (
            'book',
            'progress',
        )
        exclude = []
