"""Command to create default super user."""

from django.core.management import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    """create a default super user when building the application for the first time."""

    help = __doc__

    def handle(self, *args, **options):
        """Create default super user."""
        if not User.objects.filter(username='root').first():
            user = User.objects.create_superuser('root', 'root@admin.com', 'root')
            print("Default super user created:", user.username)

        else:
            print("Default super user already exists")
