"""Books models."""

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django_common.auth_backends import User
from model_utils import Choices

from rest_framework.authtoken.models import Token

from taggit.managers import TaggableManager


# ------- start mixins


class ModifiedModelMixin(models.Model):
    """Modified field mixin.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
    )


class PreserveModelMixin(ModifiedModelMixin):
    """Base model to handle core objects.

    Defines created, modified, and deleted fields.
    Prevents deletion of this model and flags for exclusion from results.
    """

    deleted_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
    )


# ------- end mixins


# ------- start app: meta_info


class Tag(models.Model):
    """Tag model.

    Consider an extension of tags to allow tagging with all media types.
    """

    copy = models.CharField(
        max_length=200,
    )
    slug = models.SlugField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name="tag_tags+",
        verbose_name=_('Tags'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )

    def __str__(self):
        """Return the string representation."""
        return self.name


class Meta(ModifiedModelMixin):
    """Meta model."""

    key = models.CharField(
        max_length=200,
    )
    value = models.TextField()
    tags = models.ManyToManyField(
        'Tag',
        related_name="meta_tags+",
        verbose_name=_('Tags'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )


# ------- end app: meta_info


# meta_information_example = {
#     'genre': [],
#     'author': '',
#     'collaborators': [],
#     'publisher': '',
#     'distributor': '',
#     'published_date': '',
#     'publication_issue': '',
#     'isbn': '',
#     'barcode': '',
#     'pages': '',
#     'reviews': [],
# }
# GENRES = Choices(
#     ('action', _('Action')),
#     ('adventure', _('Adventure')),
#     ('romance', _('Romance')),
#     ('fiction', _('Fiction')),
#     ('fantasy', _('Fantasy')),
#     ('non-fiction', _('Non Fiction')),
#     ('science-fiction', _('Science Fiction')),
#     ('satire', _('Satire')),
#     ('drama', _('Drama')),
#     ('mystery', _('Mystery')),
#     ('poetry', _('Poetry')),
#     ('comics', _('Comics')),
#     ('horror', _('Horror')),
#     ('art', _('Art')),
#     ('diaries', _('Diaries')),
#     ('guide', _('Guide')),
#     ('travel', _('Travel')),
# )


class Book(PreserveModelMixin):
    """Books model."""

    title = models.CharField(
        max_length=200,
    )
    description = models.TextField(
        blank=True,
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name="book_tags+",
        verbose_name=_('Tags'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )
    meta = models.ForeignKey(
        'Meta',
        related_name="book_meta+",
        verbose_name=_('Meta Information'),
        blank=True,
    )

    def __str__(self):
        """Return the string representation."""
        return self.title


class BookProgress(Meta, PreserveModelMixin):
    """Favourite books model."""

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    percent = models.FloatField(
        blank=True,
    )
    page = models.PositiveSmallIntegerField(
        blank=True,
    )
    progress = models.BigIntegerField(
        blank=True,
    )
    book = models.ForeignKey(
        'Book',
        related_name="book_progress+",
        verbose_name=_('Book'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        """Return the string representation."""
        return self.book.title


class BookReview(Meta, PreserveModelMixin):
    """Favourite books model."""

    book = models.ForeignKey(
        'Book',
        related_name="book_reviews",
        verbose_name=_('Book'),
        on_delete=models.PROTECT,
        blank=True,
    )
    progress = models.ForeignKey(
        'BookProgress',
        related_name="book_review_progress",
        verbose_name=_('Book Progress'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        """Return the string representation."""
        return self.book.title


# ------- start app: user_profile


class Profile(models.Model):
    """Profile model."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    mobile_number = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
    )

    def __str__(self):
        """Return the string representation."""
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile when an user instance is created."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Update profile when user is updated."""
    instance.profile.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Generate authentication API token for a created user instance."""
    if created:
        Token.objects.create(user=instance)


# ------- end app: user_profile
