"""General mixins."""

from django.db import models

from django.utils.timezone import now

from bookworm.managers import PreserveModelManager


def get_default_now():
    return now(USE_TZ=True)


class ModifiedModelMixin(models.Model):
    """Modified field mixin.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    modified_at = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
    )

    class Meta:
        abstract=True


class PreserveModelMixin(models.Model):
    """Base model to handle core objects.

    Defines created, modified, and deleted fields.
    Prevents deletion of this model and flags for exclusion from results.
    """

    deleted_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )

    objects = PreserveModelManager()

    class Meta:
        abstract=True

    def delete(self, *args, **kwargs):
        instance.deleted_at = now(USE_TZ=True)
        self.save()
