"""Meta Information models."""

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from hashid_field import HashidAutoField

from bookworm.mixins import ModifiedModelMixin


class Tag(models.Model):
    """Tag model.

    Consider an extension of tags to allow tagging with all media types.
    """

    id = HashidAutoField(primary_key=True)
    slug = models.SlugField(
        db_index=True,
        unique=True,
        blank=True,
    )
    slug_u = models.SlugField(
        blank=True,
    )
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

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class MetaInfoMixin(models.Model):
    """Meta mixin model."""

    id = HashidAutoField(primary_key=True)
    copy = models.TextField(
        db_index=True,
        blank=True,
        null=True,
    )
    json = JSONField(
        default={},
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="tags+",
        verbose_name=_('Tags'),
        blank=True,
    )

    class Meta:
        abstract = True


class MetaInfo(MetaInfoMixin, ModifiedModelMixin):
    """Meta model."""

    class Meta:
        verbose_name = 'Meta'
        verbose_name_plural = 'Metas'


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
