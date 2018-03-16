"""Books admin."""

from django.contrib import admin
from .models import (
    Profile,
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
