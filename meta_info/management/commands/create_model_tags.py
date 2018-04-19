"""Command to create default super user."""

import importlib

from django.core.management import BaseCommand

from meta_info.models import Tag


def class_for_name(module_name, class_name):
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c


class Command(BaseCommand):
    """Load tags from models."""

    help = __doc__

    def handle(self, *args, **options):
        """load models and check for tags to be created."""
        model_list = [
            ('authentication.models', 'TAGS', ),
            ('books.models', 'TAGS', ),
        ]
        for model_rep in model_list:
            tag_list = class_for_name(model_rep[0], model_rep[1])
            for tag in tag_list:
                if Tag.objects.filter(copy=tag).count():
                    continue
                Tag.objects.create(copy=tag)
