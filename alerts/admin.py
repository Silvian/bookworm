"""Alerts admin."""

from django.contrib import admin

from .models import SMSAlert


@admin.register(SMSAlert)
class SMSAlertAdmin(admin.ModelAdmin):
    """SMSAlert admin."""

    list_display = (
        'name',
        'send_alert',
    )
