"""Command to create default super user."""

import logging

from django.core.management import BaseCommand

from meta_info.models_localisation import LanguageTag
from meta_info.data.languages import LANGUAGES


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Load tags from models."""

    help = __doc__

    def handle(self, *args, **options):
        """load models and check for tags to be created."""
        for language in LANGUAGES:
            if LanguageTag.objects.filter(copy=language[1]).count() > 0:
                continue
            LanguageTag.objects.create(
                copy=language[1],
                family=language[0],
                name_native=language[2],
                iso_639_1=language[3],
                iso_639_2_t=language[4],
                iso_639_2_b=language[5],
                iso_639_3=language[6],
                notes=language[7],
            )
            logger.info('Added Language tag: {}'.format(language[6]))
