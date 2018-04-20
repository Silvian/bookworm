"""Meta Information models."""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from hashid_field import HashidAutoField

from meta_info.models import TagMixin
from bookworm.mixins import PreserveModelMixin


class LanguageTag(TagMixin, PreserveModelMixin):
    """Language object."""

    family = models.TextField(
        blank=True,
    )
    name_native = models.TextField(
        blank=True,
    )
    iso_639_1 = models.CharField(
        max_length=3,
        blank=True,
    )
    iso_639_2_t = models.CharField(
        max_length=3,
        db_index=True,
    )
    iso_639_2_b = models.CharField(
        max_length=3,
        db_index=True,
    )
    iso_639_3 = models.CharField(
        max_length=9,
        db_index=True,
    )
    notes = models.TextField(
        blank=True,
        default='',
    )

    class Meta:
        verbose_name = 'Language Tag'
        verbose_name_plural = 'Language Tags'

    def __str__(self):
        """ISO and name of language."""
        return '{} "{}"'.format(self.iso_639_3, self.copy[:30])


class LocationTag(TagMixin, PreserveModelMixin):
    """Language object."""

    iso_alpha_2 = models.CharField(
        max_length=3,
        db_index=True,
    )
    iso_alpha_3 = models.CharField(
        max_length=3,
        db_index=True,
    )
    iso_numeric = models.PositiveIntegerField(
        blank=True,
    )
    parent_location = models.ForeignKey(
        'LocationTag',
        related_name='child_locations+',
        verbose_name=_('Parent Location'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    default_language = models.ForeignKey(
        LanguageTag,
        related_name='default_location_language+',
        verbose_name=_('Default Location Language'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    # TODO: long_lat  # noqa

    class Meta:
        verbose_name = 'Location Tag'
        verbose_name_plural = 'Location Tags'

    def __str__(self):
        """ISO and name of location."""
        return '{} "{}"'.format(self.iso_alpha_3, self.copy[:30])


class LocaliseTag(PreserveModelMixin):
    """Localisation Tag for translation assistance."""

    id = HashidAutoField(primary_key=True)
    language = models.ForeignKey(
        LanguageTag,
        related_name='locale_language+',
        verbose_name=_('Localised Language Tag'),
        on_delete=models.DO_NOTHING,
    )
    location = models.ForeignKey(
        LocationTag,
        related_name='locale_language+',
        verbose_name=_('Localised Language Tag'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Localisation Tag'
        verbose_name_plural = 'Localisation Tags'

    @property
    def display_code(self):
        return '{}-{}'.format(
            self.language.iso_639_3,
            self.location.iso_alpha_3.lower() if self.location else ''
        )

    def __str__(self):
        """ISO codes of language and location."""
        return self.display_code
