"""Books admin."""

from django.contrib import admin
from profiles.models import (
    Profile,
    ContactMethod,
)


@admin.register(ContactMethod)
class ContactMethodAdmin(admin.ModelAdmin):
    """Profile admin."""

    list_display = (
        'type',
        'detail',
        'email',
        'uri',
        'profile',
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin."""

    list_display = (
        'name_title',
        'name_first',
        'name_family',
        'name_display',
        'email',
        'user',
    )
