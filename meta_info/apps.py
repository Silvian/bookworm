from django.apps import AppConfig


class MetaInfoConfig(AppConfig):
    name = 'meta_info'
    verbose_name = 'Meta Information'

    def ready(self):
        from meta_info import models_localisation  # noqa
        from meta_info import signals  # noqa
