"""General mixins."""

import json

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from bookworm.managers import PreserveModelManager
from bookworm.exceptions import PublishableObjectNotDefined
from authentication.models import Profile
from meta_info.models import MetaInfo


class CreatedModelMixin(models.Model):
    """Modified field mixin.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class ModifiedModelMixin(CreatedModelMixin):
    """Modified field mixin.
    """

    modified_at = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
    )

    class Meta:
        abstract = True


class PreserveModelMixin(ModifiedModelMixin):
    """Base model to handle core objects.

    Defines created, modified, and deleted fields.
    Prevents deletion of this model and flags for exclusion from results.
    """

    deleted_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )

    objects = PreserveModelManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.deleted_at = now(USE_TZ=True)
        self.save()
        return super().delete(*args, **kwargs)


class ProfileReferredMixin(models.Model):
    """Profile association mixin."""

    profile = models.ForeignKey(
        Profile,
        related_name='+',
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        abstract = True


class PublishableModelMixin(models.Model):
    """Enable a model to be publishable and visible to public view."""

    published_content = models.ForeignKey(
        'MetaInfo',
        related_name='published_content+',
        verbose_name=_('Published Content'),
        on_delete=models.CASCADE,
        null=True,
    )
    published_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )

    @property
    def published(self):
        return bool(self.published_at)

    def publish(self):
        """Create a new snapshot of this model defined by Publishable sub-class.

        All new snapshots override the previous.
        Old snapshots are retained but not assigned to this model."""
        publish_info = getattr(self, 'Publishable', None)
        if not publish_info:
            raise PublishableObjectNotDefined(self, 'publish')
        publish_info = publish_info()
        publish_dict = {
            'source': {
                'id': self.id,
                'class': self.__class__,
            },
        }
        for item in publish_info.fields:
            item_str = item
            if type(item) is tuple or type(item) is list:
                item_str = item[0]
                item_properties = item[1].split()
            item_output = getattr(self, item_str, None)
            # For query fields fetch and check content for Publishable
            if hasattr(item_output, 'all') and hasattr(item_output, 'filter'):
                child_list = list(item_output.all())
                child_output = []
                for child in child_list:
                    if item_properties:
                        child_output.append({
                            p: getattr(child, p) for p in item_properties
                        })
                    elif hasattr(item_output, 'Publishable', None):
                        child_output.append(child.publish())
                    else:
                        child_output.append(child)
                publish_dict.update({item_str: child_output, })
            else:
                if item_properties:
                    item_output = {
                        p: getattr(item_output, p) for p in item_properties
                    }
                publish_dict.update({item_str: item_output, })
            item_properties = None
        self.published_content = MetaInfo.objects.create(
            json=publish_dict,
            copy=json.dumps(publish_dict),
        )
        self.published_at = self.published_content.created_at
        self.save()
        return publish_dict

    def unpublish(self):
        """Ensure the defined publishable content is no longer available.

        All previously published content is retained as versions.
        """
        publish_info = getattr(self, 'Publishable', None)
        if not publish_info:
            raise PublishableObjectNotDefined(self, 'unpublish')
        publish_info = publish_info()
        for item in publish_info.fields:
            item_str = item
            if type(item) is tuple or type(item) is list:
                item_str = item[0]
                item_properties = item[1].split()
            item_output = getattr(self, item_str, None)
            # For query fields fetch and check content for Publishable
            if hasattr(item_output, 'all') and hasattr(item_output, 'filter'):
                child_list = list(item_output.all())
                for child in child_list:
                    publishable = hasattr(item_output, 'Publishable', None)
                    if not item_properties and publishable:
                        child.unpublish()
            elif hasattr(item_output, 'Publishable', None):
                child.unpublish()
            item_properties = None
        self.published_at = None
        self.published_content = None
        self.save()

    def unpublish_purge(self):
        """Unpublishes content and removes all history.

        Retainment of datetime stamps of previous publishes with no content."""
        self.unpublish()
        published_meta_list = MetaInfo.objects.filter(
            json__source__class=self.__class__
        )
        for item in list(published_meta_list):
            for key in item.json.keys():
                if key is not 'source':
                    item.json.pop(key)
            item.copy = json.dumps(item.json)
            item.save()

    class Meta:
        abstract = True
