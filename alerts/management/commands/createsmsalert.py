"""Command to create sms alert."""

from django.core.management import BaseCommand

from alerts.models import SMSAlert


class Command(BaseCommand):
    """create sms alert configuration data."""

    help = __doc__

    def handle(self, *args, **options):
        """Create default sms alert configuration."""
        if not SMSAlert.objects.filter(name='SMS Alerts').first():
            SMSAlert.objects.create()
            print("Created default sms alert configuration.")

        else:
            print("Default sms alert configuration already exists.")
