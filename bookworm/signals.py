"""Profile signals."""

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.timezone import now

from bookworm.mixins import PreserveModelMixin


@receiver(pre_delete, sender=PreserveModelMixin)
def pre_delete_preserve_model(sender, instance, *args, **kwargs):
    """Assign the deletion values to the instance."""
    instance.deleted_at = now(USE_TZ=True)
