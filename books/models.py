"""Books models."""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from hashid_field import HashidAutoField

from bookworm.mixins import (
    PublishableModelMixin, ProfileReferredMixin, PreserveModelMixin
)
from meta_info.models import MetaInfo
from books.serializers import (
    PublishBookSerializer,
    PublishReadingListSerializer,
    PublishBookReviewSerializer,
)


GENRES = (
    ('Action', ('Genre',), ),
    ('Adventure', ('Genre',), ),
    ('Romance', ('Genre',), ),
    ('Fiction', ('Genre',), ),
    ('Fantasy', ('Genre',), ),
    ('Non Fiction', ('Genre',), ),
    ('Science Fiction', ('Genre',), ),
    ('Satire', ('Genre',), ),
    ('Drama', ('Genre',), ),
    ('Mystery', ('Genre',), ),
    ('Poetry', ('Genre',), ),
    ('Comics', ('Genre',), ),
    ('Horror', ('Genre',), ),
    ('Art', ('Genre',), ),
    ('Diaries', ('Genre',), ),
    ('Guide', ('Genre',), ),
    ('Travel', ('Genre',), ),
)
TAGS = (
    'Genre',
    'Author',
    'Publisher',
    'Collaborator',
    'Collaborators',
    'Distributor',
    'Published Date',
    'Publication Issue',
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


class Book(
        PublishableModelMixin,
        PublicationMixin,
        PreserveModelMixin,
):
    """Books model."""

    id = HashidAutoField(primary_key=True)
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='books+',
        verbose_name=_('Meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Publishable:
        publishable_verification = None
        publishable_children = ('reviews', )
        serializer = PublishBookSerializer

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    @property
    def author(self):
        return self.tags.filter(meta_info__tags__slug__iexact='author').first()

    def __str__(self):
        """Title and author of book."""
        return '{} by {}'.format(self.title, self.author.copy)


class BookProgress(
        ProfileReferredMixin,
        PreserveModelMixin,
):
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


class BookChapter(PreserveModelMixin):
    """Book chapter model."""

    id = HashidAutoField(primary_key=True)
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
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='book_chapters+',
        verbose_name=_('Meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Book chapter'
        verbose_name_plural = 'Books\' chapters'


class ReadingList(
        PublishableModelMixin,
        ProfileReferredMixin,
        PreserveModelMixin,
):
    """Reading list model."""

    id = HashidAutoField(primary_key=True)
    title = models.CharField(
        max_length=200,
        db_index=True,
    )
    books = models.ManyToManyField(
        Book,
        related_name='reading_lists',
        verbose_name=_('Books'),
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='reading_lists+',
        verbose_name=_('Meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Publishable:
        publishable_verification = None
        publishable_children = None
        serializer = PublishReadingListSerializer

    class Meta:
        verbose_name = 'Reading List'
        verbose_name_plural = 'Reading Lists'


class BookReview(
        PublishableModelMixin,
        ProfileReferredMixin,
        PreserveModelMixin,
):
    """Book reviews model."""

    TYPES = Choices(
        (0, 'review', _('Review')),
        (1, 'footnote', _('Footnote')),
        (2, 'margin', _('Margin note')),
        (3, 'line', _('Line highlight')),
        (4, 'paragraph', _('Paragraph highlight')),
    )

    id = HashidAutoField(primary_key=True)
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
    reading_list = models.ForeignKey(
        ReadingList,
        related_name='reviews',
        verbose_name=_('Reading List'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='book_reviews+',
        verbose_name=_('Meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Publishable:
        publishable_verification = None
        publishable_children = None
        serializer = PublishBookReviewSerializer

    class Meta:
        verbose_name = 'Book review'
        verbose_name_plural = 'Books\' reviews'
