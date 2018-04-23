"""Tag signals."""
import json

from django.db.models.signals import pre_save
from django.dispatch import receiver

from meta_info.models import MetaInfo
from books.models import Book, BookChapter, ReadingList, BookReview


@receiver(pre_save, sender=BookChapter)
@receiver(pre_save, sender=ReadingList)
@receiver(pre_save, sender=BookReview)
def pre_save_book_chapter_meta_info(sender, instance, created, **kwargs):
    """set meta info for instance."""
    if not created:
        return
    instance.meta_info = MetaInfo.objects.create()


@receiver(pre_save, sender=Book)
def pre_save_book_meta_info(sender, instance, created, **kwargs):
    """Set the slug of the provided tag."""
    if not created:
        return
    instance.meta_info = MetaInfo.objects.create()
    default_json = {
        'genre': '',
        'sub_genres': [],
        'author': '',
        'collaborator': [],
        'publisher': '',
        'distributor': '',
        'published_date': '',
        'publication_issue': '',
        'barcode': '',
        'pages': 0,
    }
    default_json.update(instance.meta_info.json)
    instance.meta_info.copy = json.dumps(default_json)
    instance.meta_info.json = default_json
