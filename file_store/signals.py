"""Tag signals."""

from django.db.models.signals import pre_save
from django.dispatch import receiver

from meta_info.models import MetaInfo
from file_store.models import DisplayImage, StoredFile


@receiver(pre_save, sender=DisplayImage)
@receiver(pre_save, sender=StoredFile)
def pre_save_add_meta_info(sender, instance, *args, **kwargs):
    """set meta info for instance."""
    if not instance.pk and not instance.meta_info:
        instance.meta_info = MetaInfo.objects.create()


@receiver(pre_save, sender=DisplayImage)
def pre_save_tag(sender, instance, *args, **kwargs):
    """Set the slug of the provided tag."""
    is_hero = instance.tags.filter(slug__iexact='hero')
    current_hero = DisplayImage.objects.filter(
        tags__slug__iexact='hero',
    ).first()
    if is_hero and not current_hero:
        return
    tags = list(current_hero.tags.all())
    current_hero.tags.set([t for t in tags if t.slug is not 'hero'])
