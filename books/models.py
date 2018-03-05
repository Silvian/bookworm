"""Books models."""

from django.db import models
from django.utils import timezone
from model_utils import Choices
from django.utils.translation import ugettext_lazy as _


class Author(models.Model):
    """Author model."""

    name = models.CharField(
        max_length=200,
    )
    description = models.TextField(
        blank=True,
    )

    def __str__(self):
        """Return the string representation."""
        return self.name


class Publisher(models.Model):
    """Publisher model."""

    name = models.CharField(
        max_length=200,
    )
    description = models.TextField(
        blank=True,
    )

    def __str__(self):
        """Return the string representation."""
        return self.name


class Book(models.Model):
    """Books model."""

    GENRES = Choices(
        ('action', _('Action')),
        ('adventure', _('Adventure')),
        ('romance', _('Romance')),
        ('fiction', _('Fiction')),
        ('fantasy', _('Fantasy')),
        ('non-fiction', _('Non Fiction')),
        ('science-fiction', _('Science Fiction')),
        ('satire', _('Satire')),
        ('drama', _('Drama')),
        ('mystery', _('Mystery')),
        ('poetry', _('Poetry')),
        ('comics', _('Comics')),
        ('horror', _('Horror')),
        ('art', _('Art')),
        ('diaries', _('Diaries')),
        ('guide', _('Guide')),
        ('travel', _('Travel')),
    )

    title = models.CharField(
        max_length=200,
    )
    genre = models.CharField(
        max_length=20,
        choices=GENRES,
        default=GENRES.action,
    )
    description = models.TextField(
        blank=True,
    )
    authors = models.ManyToManyField(
        Author,
        related_name="+",
        verbose_name=_('author'),
        blank=True,
    )
    publisher = models.ForeignKey(
        Publisher,
        related_name="+",
        verbose_name=_('publisher'),
        on_delete=models.CASCADE,
        blank=True,
    )
    published_date = models.DateField(
        blank=True,
    )
    pages = models.IntegerField(
        blank=True,
        null=True,
    )
    read = models.BooleanField(
        default=False,
    )
    date_read = models.DateField(
        blank=True,
        null=True,
    )

    def mark_date_read(self):
        """Mark date when book was read."""
        self.date_read = timezone.now()

    def clean_fields(self, exclude=None):
        """Clean the fields needed for django admin."""
        if self.read:
            self.mark_date_read()
        super().clean_fields(exclude=exclude)

    def publish(self):
        """Publish book."""
        self.save()

    def __str__(self):
        """Return the string representation."""
        return self.title


class ReadingList(models.Model):
    """Reading list model."""

    name = models.CharField(
        max_length=200,
    )
    books = models.ManyToManyField(
        Book,
        related_name="reading_list",
        verbose_name=_('books'),
        blank=True,
    )

    def publish(self):
        """Publish reading list."""
        self.save()

    def __str__(self):
        """Return the string representation."""
        return self.name
