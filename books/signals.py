"""Tag signals."""

from django.db.models.signals import pre_save
from django.dispatch import receiver

from books.models import Book


@receiver(pre_save, sender=Book)
def pre_save_tag(sender, instance, *args, **kwargs):
    """Set the slug of the provided tag."""
    if instance.pk:
        return

    default_json = {
        'genre': '',
        'sub_genres': [],
        'author': '',
        'collaborator': [],
        'publisher': '',
        'distributor': '',
        'published_date': '',
        'publication_issue': '',
        'isbn': '',
        'barcode': '',
        'pages': 0,
        'chapters': [],
        'reviews': [],
    }
    default_json.update(instance.json)
    instance.json = default_json


# {
#     'title': '',
#     'page': 0,
# },
