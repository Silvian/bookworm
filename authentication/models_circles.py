"""Profile models."""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from hashid_field import HashidAutoField

from bookworm.mixins import (ProfileReferredMixin, PreserveModelMixin)
from books.models import ReadingList
from meta_info.models import MetaInfo
from authentication.models import Profile


class Circle(PreserveModelMixin):
    """Profile and group relationship model."""

    PREFIX = '¶'  # Pilcrow

    id = HashidAutoField(primary_key=True)
    title = models.CharField(
        max_length=254,
        db_index=True,
    )
    created_by = models.ForeignKey(
        Profile,
        related_name='circles',
        verbose_name=_('Room requested by'),
        on_delete=models.DO_NOTHING,
        null=True,
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='circles_meta+',
        verbose_name=_('Circles meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    reading_list = models.ManyToManyField(
        ReadingList,
        related_name='circles',
        verbose_name=_('Reading List'),
        blank=True,
    )

    @property
    def count(self):
        """Number of Profiles accepted into Circle."""
        return self.invitations.filter(
            status=Invitation.STATUSES.accepted
        ).count()

    def save(self):
        if not self.meta_info:
            self.meta_info = MetaInfo.objects.create()
        super().save()

    class Meta:
        verbose_name = 'Circle'
        verbose_name_plural = 'Circles'

    def __str__(self):
        """Valid email output of profile."""
        return '{}{}'.format(self.PREFIX, self.title or self.id)


class Invitation(ProfileReferredMixin, PreserveModelMixin):
    """Invitiation between a circle and a Profile.

    The current user requesting the invitation is defined as `self.profile`.
    """

    STATUSES = Choices(
        (0, 'invited', _('Invited')),
        (1, 'accepted', _('Accepted')),
        (2, 'rejected', _('Rejected')),
        (3, 'withdrawn', _('Withdrawn')),
        (4, 'banned', _('Banned')),
    )

    id = HashidAutoField(primary_key=True)
    status = models.IntegerField(
        choices=STATUSES,
        default=STATUSES.invited,
        blank=True,
    )
    profile_to = models.ForeignKey(
        Profile,
        related_name='invitations',
        verbose_name=_('Profile Invited'),
        on_delete=models.DO_NOTHING,
    )
    circle = models.ForeignKey(
        Circle,
        related_name='invitations',
        verbose_name=_('Circle invited to'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='invitation_meta+',
        verbose_name=_('Invitation meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    def save(self):
        if not self.meta_info:
            self.meta_info = MetaInfo.objects.create()
        super().save()

    class Meta:
        verbose_name = 'Invitation'
        verbose_name_plural = 'Invitations'

    def __str__(self):
        """Short description of what this invitation is intended."""
        rtn = 'Invitation to: {}, for: {}'.format(
            self.profile_to, self.circle if self.circle else self.profile)
        if self.circle:
            rtn += ', from: {}'.format(self.circle)
        return rtn
