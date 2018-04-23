"""FileStore models."""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from hashid_field import HashidAutoField

from bookworm.mixins import (
    ProfileReferredMixin,
    PreserveModelMixin,
)
from meta_info.models import MetaInfo


TAGS = (
    'Hero',
)


class FileMixin(models.Model):
    """Mixin for a basic file model."""

    id = HashidAutoField(primary_key=True)
    title = models.CharField(
        max_length=200,
        db_index=True,
        blank=True,
    )
    description = models.TextField(
        blank=True,
    )
    extension = models.CharField(
        max_length=20,
        blank=True,
    )
    mime = models.CharField(
        max_length=50,
        blank=True,
    )
    progress = models.ForeignKey(
        'books.BookProgress',
        related_name='file_progress+',
        verbose_name=_('Progress'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='files+',
        verbose_name=_('Meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class DisplayImage(
        FileMixin,
        ProfileReferredMixin,
        PreserveModelMixin,
):
    """Image model.

    TODO: Make this model publishable with `PublishableModelMixin`.  # noqa
    """

    image = models.ImageField()
    original = models.ForeignKey(
        'DisplayImage',
        related_name='sizes',
        verbose_name=_('Cropped Images'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    circle = models.ForeignKey(
        'authentication.Circle',
        related_name='images',
        verbose_name=_('Circles\' image'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    book = models.ForeignKey(
        'books.Book',
        related_name='images',
        verbose_name=_('Book'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'


class StoredFile(
        FileMixin,
        ProfileReferredMixin,
        PreserveModelMixin,
):
    """Publication file model.

    TODO: If self.url is defined scrape file.  # noqa
    TODO: Make this model publishable with `PublishableModelMixin`.  # noqa
    """

    file = models.FileField(
        null=True,
    )
    url = models.URLField(
        max_length=2000,
        blank=True,
        null=True,
    )
    book = models.ForeignKey(
        'books.Book',
        related_name='files',
        verbose_name=_('Book'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Publication File'
        verbose_name_plural = 'Publications\' Files'
