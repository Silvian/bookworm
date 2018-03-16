"""Books models."""

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django_common.auth_backends import User

from django.contrib.postgres.fields import HStoreField

from model_utils import Choices

from profile.models import Profile

from rest_framework.authtoken.models import Token


class Book(Meta, PreserveModelMixin):
    """Books model."""

    title = models.CharField(
        max_length=200,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )


class BookProgress(PreserveModelMixin):
    """Book progress model."""

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
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
        'Book',
        related_name="progress+",
        verbose_name=_('Book'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.DO_NOTHING,
    )


class BookReview(Meta, PreserveModelMixin):
    """Book reviews model."""

    book = models.ForeignKey(
        'Book',
        related_name="reviews",
        verbose_name=_('Book'),
        on_delete=models.PROTECT,
    )
    progress = models.ForeignKey(
        'BookProgress',
        related_name="review_progress",
        verbose_name=_('Book Progress'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.DO_NOTHING,
    )
