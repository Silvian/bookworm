"""Books admin."""

from django.contrib import admin
from .models import (
    Author,
    Publisher,
    Book,
    ReadingList,
)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Author admin."""

    list_display = ('name',)

    search_fields = ('name',)


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

    list_filter = (
        'genre',
    )


@admin.register(ReadingList)
class ReadingList(admin.ModelAdmin):
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
    )

    list_filter = (
        'started_reading',
        'finished_reading',
        'book__genre',
    )
