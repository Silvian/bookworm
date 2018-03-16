"""Meta Information admin."""

from django.contrib import admin
from .models import (
    Tag,
    MetaInfo,
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag admin."""

    list_display = (
        'slug',
        'copy',
    )
    search_fields = ('copy',)


@admin.register(MetaInfo)
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin."""

    list_display = (
        'copy',
        'json',
    )
    search_fields = ('copy',)
