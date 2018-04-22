"""Profile models."""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices

from bookworm.mixins import (ProfileReferredMixin, PreserveModelMixin)
from books.models import ReadingList
from meta_info.models import (MetaInfoMixin, MetaInfo)
from authentication.models import (Profile, ContactMethod)


class Circle(PreserveModelMixin):
    """Profile and group relationship model."""

    PREFIX = '¶'  # Pilcrow

    title = models.CharField(
        max_length=254,
        db_index=True,
        blank=True,
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='circles_meta+',
        verbose_name=_('Circles meta data'),
        on_delete=models.DO_NOTHING,
    )
    created_by = models.ForeignKey(
        Profile,
        related_name='circles',
        verbose_name=_('Room requested by'),
        on_delete=models.DO_NOTHING,
    )
    admins = models.ManyToManyField(
        Profile,
        related_name='circles_administrators',
        verbose_name=_('Administrators of this Circle'),
        blank=True,
    )
    reading_list = models.ForeignKey(
        ReadingList,
        related_name='circles',
        verbose_name=_('Reading List'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )

    class Meta:
        verbose_name = 'Circle'
        verbose_name_plural = 'Circles'

    def __str__(self):
        """Valid email output of profile."""
        return '{}{}'.format(self.PREFIX, self.title or self.id)


class CircleContactMethod(MetaInfoMixin, PreserveModelMixin):
    """Contact lists for a circle."""

    contacts = models.ManyToManyField(
        ContactMethod,
        related_name='circle_contacts+',
        verbose_name=_('Contact details'),
        on_delete=models.DO_NOTHING,
    )
    circle = models.ForeignKey(
        Circle,
        related_name='contacts',
        verbose_name=_('Circle'),
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        verbose_name = 'Circle Contact Method'
        verbose_name_plural = 'Circles\' Contact Methods'

    def __str__(self):
        """Valid email output of profile."""
        return '{}, contacts[{}]'.format(self.circle, len(self.contacts))


class Invitation(ProfileReferredMixin, PreserveModelMixin):
    """Invitiation between a circle and a Profile.

    The current user requesting the invitation is defined as `self.profile`.
    """

    STATUSES = Choices(
        (0, 'invited', _('Invited')),
        (1, 'in', _('In')),
        (2, 'rejected', _('Rejected')),
        (3, 'withdrawn', _('Withdrawn')),
        (4, 'banned', _('Banned')),
    )

    status = models.IntegerField(
        choices=STATUSES,
        default=STATUSES.invited,
        blank=True,
    )
    profile_to = models.ForeignKey(
        Profile,
        related_name='invitations',
        verbose_name=_('Invitation'),
    )
    circle = models.ForeignKey(
        Circle,
        related_name='invitations',
        verbose_name=_('Circle invited to'),
        blank=True,
        null=True,
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='invitation_meta+',
        verbose_name=_('Invitation meta data'),
        on_delete=models.DO_NOTHING,
    )

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


class DisplayImage(PreserveModelMixin):
    """Publication file model.

    TODO: Move this to a media management application.  # noqa

    TODO: Have the image manager handle the relation to other objects.  # noqa
    """

    image = models.ImageField()
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='images_meta+',
        verbose_name=_('Image meta data'),
        on_delete=models.DO_NOTHING,
    )
    uploaded_by = models.ForeignKey(
        Profile,
        related_name='images+',
        verbose_name=_('Uploaded by profile'),
        on_delete=models.DO_NOTHING,
    )
    sizes = models.ManyToManyField(
        'DisplayImage',
        related_name='original_image+',
        verbose_name=_('Cropped Images'),
    )

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
