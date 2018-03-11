"""Alerts services."""
from django.conf import settings
import requests


class SMSService:
    """SMS service."""

    service_url = ''
    api_token = ''

    def __init__(self, service_url=settings.SMS_URL, api_token=settings.SMS_TOKEN):
        self.service_url = service_url
        self.api_token = api_token

    def send_alert(self, message, mobile):
        """Send alerts."""
        response = requests.post(self.service_url, {
            'phone': mobile,
            'message': message,
            'key': self.api_token,
        }).json()

        return response
