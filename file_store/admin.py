"""FileStore admin."""

from django.contrib import admin

from file_store.models import (
    DisplayImage,
    StoredFile,
)


@admin.register(DisplayImage)
class DisplayImageAdmin(admin.ModelAdmin):
    """DisplayImage admin."""

    list_display = (
        'id',
        'title',
        'description',
        'image'
    )
    search_fields = (
        'title',
        'tags__copy',
    )
    list_filter = ('title',)
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )


@admin.register(StoredFile)
class StoredFileAdmin(admin.ModelAdmin):
    """StoredFile admin."""

    list_display = (
        'id',
        'title',
        'description',
        'file',
        'url',
    )
    search_fields = (
        'title',
        'tags__copy',
    )
    list_filter = ('title',)
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )
