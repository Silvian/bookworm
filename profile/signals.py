"""Profile signals."""

from django.conf import settings
from django.db.models.signals import (pre_save, post_save)
from django.dispatch import receiver
from django_common.auth_backends import User

from meta_info.models import (Tag, Meta)
from profile.models import (Profile, ContactMethod)

from rest_framework.authtoken.models import Token


@receiver(pre_save, sender=ContactMethod)
def pre_save_contact_method(sender, instance, *args, **kwargs):
    """Assign fields expected for ContactMethod."""
    if instance.type == ContactMethod.TYPES.email and not instance.email:
        instance.email = instance.detail


@receiver(post_save, sender=ContactMethod)
def pre_save_contact_method(sender, instance, *args, **kwargs):
    """Set b y default the primary tag for ContactMethod."""
    require_primary = [
        ContactMethod.TYPES.email,
        ContactMethod.TYPES.mobile
    ]
    if instance.type in require_primary:
        contacts = ContactMethod.objects.filter(
            profile=instance.profile,
            type=instance.type,
            tags__slug=ContactMethod.TAGS.primary,
        ).count()
        tag = Tag.objects.get(slug=ContactMethod.TAGS.primary)
        if not contacts:
            instance.tags.add(tag)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile when an user instance is created."""
    if not created:
        return
    meta = Meta()
    Profile.objects.create(
        user=instance,
        meta=meta,
    )


@receiver(post_save, sender=User)
def post_save_user_profile(sender, instance, **kwargs):
    """Update profile when user is updated."""
    instance.profile.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Generate authentication API token for a created user instance."""
    if created:
        Token.objects.create(user=instance)
