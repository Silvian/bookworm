"""Profile models."""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_common.auth_backends import User

from model_utils import Choices
from hashid_field import HashidAutoField

from bookworm.mixins import (PreserveModelMixin, ModifiedModelMixin)
from meta_info.models import (MetaInfoMixin, MetaInfo)


class ContactMethod(MetaInfoMixin, PreserveModelMixin, ModifiedModelMixin):
    """Contact method."""

    TYPES = Choices(
        (0, 'email', _('email')),
        (1, 'mobile', _('mobile number')),
        (2, 'landline', _('landline number')),
        (3, 'postal', _('postal address')),
        (4, 'billing', _('billing address')),
        (5, 'social', _('social network id')),
    )

    TAGS = Choices(
        ('primary', _('primary')),
        ('billing', _('billing')),
    )

    type = models.IntegerField(
        choices=TYPES,
        default=TYPES.email,
    )
    detail = models.TextField(
        db_index=True,
    )
    email = models.EmailField(
        max_length=254,
        db_index=True,
        unique=True,
        blank=True,
        null=True,
    )
    uri = models.URLField(
        blank=True,
        null=True,
    )
    profile = models.ForeignKey(
        'Profile',
        related_name="contacts",
        verbose_name=_('Contact details profile'),
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        verbose_name = 'Contact Method'
        verbose_name_plural = 'Contact Methods'


class Profile(PreserveModelMixin, ModifiedModelMixin):
    """Profile model."""

    NAME_TITLES = Choices(
        (0, 'mrs', _('Mrs')),
        (1, 'mr', _('Mr')),
        (2, 'miss', _('Miss')),
        (3, 'ms', _('Ms')),
        (4, 'dr', _('Dr')),
        (5, 'sir', _('Sir')),
    )

    id = HashidAutoField(primary_key=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    name_title = models.IntegerField(
        choices=NAME_TITLES,
        blank=True,
        null=True,
    )
    name_first = models.CharField(
        max_length=64,
        db_index=True,
    )
    name_family = models.CharField(
        max_length=64,
        db_index=True,
    )
    name_middle = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )
    name_display = models.CharField(
        max_length=254,
    )
    email = models.EmailField(
        max_length=254,
        db_index=True,
        unique=True,
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name="profile_meta+",
        verbose_name=_('Profile meta data'),
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
