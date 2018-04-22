"""Meta Information models."""

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from hashid_field import HashidAutoField

from bookworm.mixins import PreserveModelMixin


class TagMixin(models.Model):
    """Tagging base mixin."""

    id = HashidAutoField(primary_key=True)
    slug = models.SlugField(
        db_index=True,
        unique=True,
        blank=True,
    )
    copy = models.CharField(
        max_length=200,
        db_index=True,
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='tag_tags+',
        verbose_name=_('Tags'),
        blank=True,
    )

    class Meta:
        abstract = True


class Tag(TagMixin, PreserveModelMixin):
    """Tag model."""

    PREFIX = '#'  # hash

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        """Display only as URI valid slug."""
        return '{}{}'.format(self.PREFIX, self.copy)


class MetaInfoMixin(models.Model):
    """Meta mixin model."""

    id = HashidAutoField(primary_key=True)
    copy = models.TextField(
        db_index=True,
        blank=True,
    )
    json = JSONField(
        default={},
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags+',
        verbose_name=_('Tags'),
        blank=True,
    )

    class Meta:
        abstract = True


class MetaInfo(MetaInfoMixin, PreserveModelMixin):
    """Meta model."""

    uri = models.URLField(
        max_length=2000,
        blank=True,
        null=True,
    )
    chain = models.ManyToManyField(
        'MetaInfo',
        verbose_name=_('Meta Data Chain'),
        blank=True,
    )

    class Meta:
        verbose_name = 'Meta'
        verbose_name_plural = 'Metas'

    def __str__(self):
        """Represent MetaInfo in brevity from complex store."""
        description = self.copy if self.copy else self.uri
        if not self.copy:
            description = 'meta empty'
        return '{} "{}" tags:{}'.format(
            self.id,
            description[:20],
            self.tags.count()
        )
