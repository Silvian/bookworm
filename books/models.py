"""Books models."""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from hashid_field import HashidAutoField

from bookworm.mixins import (PreserveModelMixin, ModifiedModelMixin)
from profiles.models import Profile
from meta_info.models import MetaInfoMixin


class Book(MetaInfoMixin, PreserveModelMixin, ModifiedModelMixin):
    """Books model."""

    id = HashidAutoField(
        primary_key=True,
        min_length=10,
    )
    title = models.CharField(
        max_length=200,
        db_index=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )


class BookProgress(PreserveModelMixin, ModifiedModelMixin):
    """Book progress model."""

    percent = models.FloatField(
        blank=True,
        null=True,
    )
    page = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )
    progress = models.BigIntegerField(
        blank=True,
        null=True,
    )
    book = models.ForeignKey(
        Book,
        related_name='progress+',
        verbose_name=_('Book progress'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.DO_NOTHING,
    )


class BookReview(MetaInfoMixin, PreserveModelMixin, ModifiedModelMixin):
    """Book reviews model."""

    book = models.ForeignKey(
        Book,
        related_name='reviews',
        verbose_name=_('Book reviews'),
        on_delete=models.PROTECT,
    )
    progress = models.ForeignKey(
        'BookProgress',
        related_name='review',
        verbose_name=_('Book review Progress'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.DO_NOTHING,
    )
