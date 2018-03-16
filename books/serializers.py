"""Books app serializers."""

from rest_framework import serializers

from meta_info.serializers import MetaSerializer
from profiles.serializers import ProfileSerializer

from books.models import (
    Book,
    BookProgress,
    BookReview,
)


class BookSerializer(MetaSerializer):
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


class BookProgressSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    profile = ProfileSerializer()

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
            'profile',
        )


class BookReviewSerializer(MetaSerializer):
    book = BookSerializer()
    progress = BookProgressSerializer()
    profile = ProfileSerializer()

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
            'profile',
        )
        exclude = []
