"""General mixins."""

from django.db import models

from django.utils.timezone import now

from bookworm.managers import PreserveModelManager


class CreatedModelMixin(models.Model):
    """Modified field mixin.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class ModifiedModelMixin(CreatedModelMixin):
    """Modified field mixin.
    """

    modified_at = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
    )

    class Meta:
        abstract = True


class PreserveModelMixin(ModifiedModelMixin):
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
        abstract = True

    def delete(self, *args, **kwargs):
        self.deleted_at = now(USE_TZ=True)
        self.save()
        return super().delete(*args, **kwargs)
