"""Profile models."""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_common.auth_backends import User

from model_utils import Choices
from hashid_field import HashidAutoField

from bookworm.mixins import PreserveModelMixin
from meta_info.models import MetaInfo


SOCIAL_PLATFORMS = (
    ('Facebook', ('social', ), ),
    ('Twitter', ('social', ), ),
    ('Google', ('social', ), ),
    ('Instagram', ('social', ), ),
    ('Pintrest', ('social', ), ),
)
TAGS = (
    'primary',
    'billing',
    'email',
    'mobile',
    'landline',
    'postal',
    'social',
) + SOCIAL_PLATFORMS


class ContactMethod(PreserveModelMixin):
    """Contact method."""

    TYPES = Choices(
        (0, 'email', _('email')),
        (1, 'mobile', _('mobile number')),
        (2, 'landline', _('landline number')),
        (3, 'postal', _('postal address')),
        (4, 'billing', _('billing address')),
        (5, 'social', _('social network id')),
    )

    id = HashidAutoField(primary_key=True)
    type = models.IntegerField(
        choices=TYPES,
        default=TYPES.email,
        blank=True,
    )
    detail = models.TextField(
        db_index=True,
    )
    email = models.EmailField(
        max_length=254,
        db_index=True,
        blank=True,
        null=True,
    )
    uri = models.URLField(
        blank=True,
        null=True,
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='contacts+',
        verbose_name=_('Meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    profile = models.ForeignKey(
        'Profile',
        related_name='contacts',
        verbose_name=_('Profile'),
        on_delete=models.DO_NOTHING,
    )
    circle = models.ForeignKey(
        'Circle',
        related_name='contacts',
        verbose_name=_('Circle'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    def save(self):
        if not self.meta_info:
            self.meta_info = MetaInfo.objects.create()
        super().save()

    class Meta:
        verbose_name = 'Contact Method'
        verbose_name_plural = 'Contact Methods'

    def __str__(self):
        """Valid email output of profile."""
        base = 'Contact {} {}'.format(self.type, self.detail)
        if self.circle:
            return '{}, circle({})'.format(self.circle)
        return base


class Profile(PreserveModelMixin):
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
        related_name='profile',
        verbose_name=_('Profiles\' User'),
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
        blank=True,
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
        related_name='profiles+',
        verbose_name=_('Meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    def save(self):
        if not self.meta_info:
            self.meta_info = MetaInfo.objects.create()
        super().save()

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    @property
    def display_name(self):
        """Generate the profiles display name when none is provided."""
        name_list = ['name_first', 'name_family']
        return self.name_display or \
            ' '.join([getattr(self, n) for n in name_list if getattr(self, n)])

    def __str__(self):
        """Valid email output of profile."""
        return '{} "{}"'.format(self.display_name or self.id, self.email)
