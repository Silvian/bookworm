"""Command to create default super user."""

import importlib
import logging

from django.core.management import BaseCommand
from django.utils.text import slugify

from meta_info.models import Tag


logger = logging.getLogger(__name__)


def class_for_name(module_name, class_name):
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c


class Command(BaseCommand):
    """Load tags from models."""

    help = __doc__

    def _update_tag_dependants(self, tag, dependant_list):
        if not dependant_list:
            return
        slug_list = [slugify(n) for n in dependant_list]
        if tag.tags.count() is 0:
            set_tags = list(Tag.objects.filter(slug__in=slug_list, ))
        else:
            tags = tag.tags.all()
            set_tags = list(tags)
            for slug in slug_list:
                if tags.filter(slug=slug).first():
                    continue
                set_tags.append(Tag.objects.filter(slug=slug).first())
        tag.tags.set(set_tags)
        tag.save()
        logger.info(
            'Tag {}, dependants set: {}'.format(tag.copy, list(set_tags), )
        )

    def _create_tags(self, tag_list):
        for tag in tag_list:
            dependant_list = ()
            if type(tag) is tuple or type(tag) is list:
                dependant_list = tag[1]
                self._create_tags(dependant_list)
                tag = tag[0]
            if Tag.objects.filter(slug=slugify(tag)).first():
                continue
            created = Tag.objects.create(copy=tag)
            logger.info('Tag created: {}'.format(tag))
            self._update_tag_dependants(created, dependant_list)

    def handle(self, *args, **options):
        """load models and check for tags to be created."""
        model_list = [
            ('authentication.models', 'TAGS', ),
            ('books.models', 'TAGS', ),
            ('file_store.models', 'TAGS', ),
            ('meta_info.data.default_tags', 'TAGS', ),
        ]
        for model_rep in model_list:
            tag_list = class_for_name(model_rep[0], model_rep[1])
            self._create_tags(tag_list)
