"""Managers for objects."""

from django.db import models


class PreserveModelManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
            deleted_at=None,
        )
