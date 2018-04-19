"""Books models."""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from hashid_field import HashidAutoField

from bookworm.mixins import PreserveModelMixin
from authentication.models import Profile
from meta_info.models import MetaInfoMixin


GENRES = (
    'Action',
    'Adventure',
    'Romance',
    'Fiction',
    'Fantasy',
    'Non Fiction',
    'Science Fiction',
    'Satire',
    'Drama',
    'Mystery',
    'Poetry',
    'Comics',
    'Horror',
    'Art',
    'Diaries',
    'Guide',
    'Travel',
)
TAGS = (
    'genre',
    'author',
    'publisher',
    'isbn',
    'collaborator',
    'collaborators',
    'distributor',
    'published date',
    'publication issue',
) + GENRES


class PublicationMixin(models.Model):
    """Publication mixin."""

    title = models.CharField(
        max_length=200,
        db_index=True,
    )
    description = models.TextField(
        blank=True,
    )
    isbn = models.CharField(
        max_length=200,
        db_index=True,
        blank=True,
    )

    class Meta:
        abstract = True


class ProfileReferredMixin(models.Model):
    """Profile association mixin."""

    profile = models.ForeignKey(
        Profile,
        related_name='+',
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        abstract = True


class Book(PublicationMixin, MetaInfoMixin, PreserveModelMixin):
    """Books model."""

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    @property
    def author(self):
        return self.tags.filter(tags__slug__iexact='author')[0]

    def __str__(self):
        """Title and author of book."""
        return '{} by {}'.format(self.title, self.author.copy)


class BookProgress(ProfileReferredMixin, PreserveModelMixin):
    """Book progress model."""

    id = HashidAutoField(primary_key=True)
    percent = models.FloatField()
    page = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )
    start = models.BigIntegerField()
    end = models.BigIntegerField(
        blank=True,
        null=True,
    )
    book = models.ForeignKey(
        Book,
        related_name='progress+',
        verbose_name=_('Book'),
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        verbose_name = 'Book progress'
        verbose_name_plural = 'Books\' progress'

    def __str__(self):
        """Title and percent of book progress."""
        return '{} at {}%'.format(self.book.title, self.percent)


class PublicationFile(MetaInfoMixin, PreserveModelMixin):
    """Publication file model."""

    file = models.FileField()
    book = models.ForeignKey(
        Book,
        related_name='files',
        verbose_name=_('Book'),
        on_delete=models.DO_NOTHING,
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
        BookProgress,
        related_name='file_progress+',
        verbose_name=_('Progress'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Publication File'
        verbose_name_plural = 'Publications\' Files'


class BookChapter(MetaInfoMixin, PreserveModelMixin):
    """Book chapter model."""

    title = models.CharField(
        max_length=200,
        db_index=True,
    )
    progress = models.ForeignKey(
        BookProgress,
        related_name='chapter_progress+',
        verbose_name=_('Progress'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )
    book = models.ForeignKey(
        Book,
        related_name='chapters',
        verbose_name=_('Book'),
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        verbose_name = 'Book chapter'
        verbose_name_plural = 'Books\' chapters'


class BookReview(ProfileReferredMixin, MetaInfoMixin, PreserveModelMixin):
    """Book reviews model."""

    TYPES = Choices(
        (0, 'review', _('Review')),
        (1, 'footnote', _('Footnote')),
        (2, 'margin', _('Margin note')),
        (3, 'line', _('Line highlight')),
        (4, 'paragraph', _('Paragraph highlight')),
    )

    type = models.IntegerField(
        choices=TYPES,
        default=TYPES.review,
        blank=True,
    )
    book = models.ForeignKey(
        Book,
        related_name='reviews',
        verbose_name=_('Book'),
        on_delete=models.PROTECT,
    )
    progress = models.ForeignKey(
        BookProgress,
        related_name='reviewed_at',
        verbose_name=_('Progress'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )

    class Meta:
        verbose_name = 'Book review'
        verbose_name_plural = 'Books\' reviews'
