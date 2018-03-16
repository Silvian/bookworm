"""Books admin."""

from django.contrib import admin

from books.models import (
    Book,
    BookProgress,
    BookReview,
)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Book admin."""

    list_display = (
        'title',
        'description',
    )

    search_fields = (
        'title',
    )

    list_filter = ('title',)


@admin.register(BookProgress)
class BookProgressAdmin(admin.ModelAdmin):
    """BookProgress admin."""

    list_display = ('book', 'profile',)

    search_fields = (
        'book__title',
        'profile__user__username',
    )

    list_filter = ('book__title',)


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    """BookReview admin."""

    list_display = (
        'book',
        'copy',
    )

    search_fields = (
        'book__title',
        'profile__user__username',
    )

    list_filter = (
        'book__title',
    )
