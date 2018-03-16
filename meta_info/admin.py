"""Meta Information admin."""

from django.contrib import admin
from .models import (
    Tag,
    Meta,
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag admin."""

    list_display = (
        'slug',
        'value',
    )
    search_fields = ('value',)


@admin.register(Meta)
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin."""

    list_display = (
        'key',
        'value',
    )
