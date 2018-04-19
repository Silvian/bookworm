"""Tag signals."""

import logging

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from meta_info.models import Tag
from meta_info.models_localisation import (LocationTag, LanguageTag)


logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Tag)
@receiver(pre_save, sender=LocationTag)
def pre_save_tag(sender, instance, *args, **kwargs):
    """Set the slug of the provided tag if none is set."""
    if instance.slug:
        return
    instance.slug = slugify(instance.copy)
    logger.debug('Tag {}.slug updated'.format(instance.copy))


@receiver(pre_save, sender=LanguageTag)
def pre_save_language_tag(sender, instance, *args, **kwargs):
    """Set the slug of the provided tag if none is set."""
    if instance.slug:
        return
    instance.slug = slugify(' '.join([instance.copy, instance.iso_639_3]))
    if len(instance.slug) > 50:
        instance.slug = '{}'.format(instance.slug[:50])
    logger.debug('Tag {}.slug updated'.format(instance.copy))
