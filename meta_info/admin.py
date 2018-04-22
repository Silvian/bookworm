"""Meta Information admin."""

from django.contrib import admin
from .models import (
    Tag,
    MetaInfo,
)
from meta_info.models_localisation import (
    LanguageTag,
    LocationTag,
    LocaliseTag,
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag admin."""

    date_hierarchy = 'created_at'
    list_display = (
        'id',
        'slug',
        'copy',
    )
    search_fields = (
        'copy',
    )
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )


@admin.register(MetaInfo)
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin."""

    list_display = (
        'id',
        'copy',
        'json',
    )
    search_fields = (
        'copy',
    )
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )


@admin.register(LanguageTag)
class LanguageTagAdmin(admin.ModelAdmin):
    """LanguageTag admin."""

    list_display = TagAdmin.list_display + (
        'name_native',
        'iso_639_3',
    )
    search_fields = TagAdmin.search_fields + (
        'name_native',
        'iso_639_1',
        'iso_639_2_t',
        'iso_639_2_b',
        'iso_639_3',
    )
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )


@admin.register(LocationTag)
class LocationTagAdmin(admin.ModelAdmin):
    """LocationTag admin."""

    list_display = TagAdmin.list_display + (
        'iso_alpha_2',
        'iso_alpha_3',
    )
    search_fields = TagAdmin.search_fields + (
        'iso_alpha_2',
        'iso_alpha_3',
    )
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )


@admin.register(LocaliseTag)
class LocaliseTagAdmin(admin.ModelAdmin):
    """LocaliseTag admin."""

    list_display = (
        'id',
        'language',
        'location',
    )
    search_fields = ('language',)
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )
