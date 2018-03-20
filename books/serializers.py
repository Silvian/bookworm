"""Books app serializers."""

from rest_framework import serializers

from books.models import (
    Author,
    Book,
    Publisher,
    ReadingList,
    Favourite,
)


class UserValidateModelSerializerMixin(serializers.ModelSerializer):
    """Provide a mixin for user validation used within serializers."""

    def validate(self, attrs):
        """Add or update favourites for authenticated user."""
        request_user = self.context['request'].user
        attrs['user'] = request_user
        return super().validate(attrs)


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = (
            'id',
            'name',
            'description',
        )
        exclude = []


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = (
            'id',
            'name',
            'description',
        )
        exclude = []


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    publisher = PublisherSerializer()

    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'genre',
            'description',
            'pages',
            'authors',
            'publisher',
            'published_date',
        )
        exclude = []

    def create(self, validated_data):
        """Create author and publisher."""
        publisher_data = validated_data.pop('publisher')
        publisher = Publisher.objects.create(**publisher_data)
        validated_data['publisher'] = publisher
        authors_data = validated_data.pop('authors')
        book = Book.objects.create(**validated_data)
        for author in authors_data:
            Author.objects.create(**author)
        return book


class ReadingListSerializer(UserValidateModelSerializerMixin):

    class Meta:
        model = ReadingList
        exclude = []
        read_only_fields = (
            'id',
            'started_date',
            'finished_date',
        )
        fields = read_only_fields + (
            'book',
            'started_reading',
            'finished_reading',
            'user',
        )


class FavouriteSerializer(UserValidateModelSerializerMixin):

    class Meta:
        model = Favourite
        fields = (
            'id',
            'book',
            'user',
        )
        exclude = []
