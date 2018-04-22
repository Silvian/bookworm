"""Books admin."""

from django.contrib import admin
from authentication.models import (
    Profile,
    ContactMethod,
)


@admin.register(ContactMethod)
class ContactMethodAdmin(admin.ModelAdmin):
    """Profile admin."""

    list_display = (
        'id',
        'type',
        'detail',
        'email',
        'uri',
    )
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin."""

    list_display = (
        'id',
        'name_title',
        'name_first',
        'name_family',
        'name_display',
        'email',
    )
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )
    readonly_fields = (
        'user',
    )
