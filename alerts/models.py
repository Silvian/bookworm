"""Alerts models."""

from django.db import models


class SingletonModel(models.Model):
    """Singleton abstract class."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Ensure that only one instance is ever saved."""
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Do not allow deleting this instance."""
        pass

    @classmethod
    def load(cls):
        """Custom method to retrieve the single object."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class SMSAlert(SingletonModel):
    """SMS Alerts model."""

    name = models.CharField(
        max_length=50,
        default='SMS Alerts',
    )
    message = models.TextField(
        default="Don't forget to continue reading"
    )
    send_alert = models.BooleanField(
        default=False,
    )

    def __str__(self):
        """Return the string representation."""
        return self.name
