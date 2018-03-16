"""Tag signals."""

from django.db.models.signals import (pre_save, post_save)
from django.dispatch import receiver
from django.utils.text import slugify

from meta_info.models import Tag


@receiver(pre_save, sender=Tag)
def pre_save_tag(sender, instance, *args, **kwargs):
    """Set the slug of the provided tag."""
    instance.slug = slugify(instance.copy)
    instance.slug_u = slugify(instance.copy, allow_unicode=True)
