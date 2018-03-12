from rest_framework import serializers

from books.models import (Book, ReadingList)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = []


class ReadingListSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = ReadingList
        exclude = []
