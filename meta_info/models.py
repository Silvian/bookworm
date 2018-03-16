"""Meta Information models."""

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from bookworm.mixins import ModifiedModelMixin


class Tag(models.Model):
    """Tag model.

    Consider an extension of tags to allow tagging with all media types.
    """

    slug = models.SlugField(
        db_index=True,
        unique=True,
    )
    slug_u = models.SlugField()
    copy = models.CharField(
        max_length=200,
        db_index=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name="tag_tags+",
        verbose_name=_('Tags'),
        blank=True,
    )


class MetaInfoMixin(models.Model):
    """Meta mixin model."""

    copy = models.TextField(
        db_index=True,
        blank=True,
        null=True,
    )
    json = JSONField(
        default={},
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="tags+",
        verbose_name=_('Tags'),
        blank=True,
    )

    class Meta:
        abstract=True


class MetaInfo(MetaInfoMixin, ModifiedModelMixin):
    """Meta model."""
    pass


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
