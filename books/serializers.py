"""Books app serializers."""

from rest_framework import serializers

from bookworm.serializers import ProfileAssociationSerializerMixin
from meta_info.serializers import MetaSerializer

from books.models import (
    Book,
    BookProgress,
    BookReview,
)


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
