from rest_framework import serializers

from books.models import (
    Author,
    Book,
    Publisher,
    ReadingList,
)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        exclude = []


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        exclude = []


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    publisher = PublisherSerializer()

    class Meta:
        model = Book
        exclude = []


class ReadingListSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = ReadingList
        exclude = []
