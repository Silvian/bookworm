"""Books admin."""

from django.contrib import admin
from .models import (
    Profile,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin."""

    list_display = (
        'user',
        'mobile_number',
        'birth_date',
    )
