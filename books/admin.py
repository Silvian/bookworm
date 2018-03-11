"""Books admin."""

from django.contrib import admin
from .models import (
    Author,
    Profile,
    Publisher,
    Book,
    Favourite,
    ReadingList,
)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Author admin."""

    list_display = ('name',)

    search_fields = ('name',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin."""

    list_display = (
        'user',
        'mobile_number',
        'birth_date',
    )


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """Publisher admin."""

    list_display = ('name',)

    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Book admin."""

    list_display = (
        'title',
        'genre',
        'pages',
        'publisher',
        'published_date',
    )

    search_fields = (
        'title',
        'genre',
        'authors__name',
        'publisher__name',
        'published_date',
    )

    list_filter = ('genre',)


@admin.register(Favourite)
class Favourite(admin.ModelAdmin):
    """Favourite admin."""

    list_display = ('book', 'user',)

    search_fields = (
        'book__title',
        'book__genre',
        'book__authors__name',
        'book__publisher__name',
        'book__published_date',
        'user__username',
    )

    list_filter = ('book__genre',)


@admin.register(ReadingList)
class ReadingListAdmin(admin.ModelAdmin):
    """ReadingList admin."""

    list_display = (
        'book',
        'started_reading',
        'started_date',
        'finished_reading',
        'finished_date',
    )

    search_fields = (
        'book__title',
        'book__genre',
        'book__authors__name',
        'book__publisher__name',
        'book__published_date',
        'user__username',
    )

    list_filter = (
        'started_reading',
        'finished_reading',
        'book__genre',
    )
