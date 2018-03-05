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
        'publisher',
        'published_date',
        'pages',
        'read',
        'date_read',
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
        'read',
    )


@admin.register(ReadingList)
class ReadingList(admin.ModelAdmin):
    """ReadingList admin."""

    list_display = (
        'name',
    )

    search_fields = (
        'books__title',
        'books__genre',
        'books__authors__name',
        'books__publisher__name',
        'books__publisher__published_date',
    )

    list_filter = ('books__read',)
