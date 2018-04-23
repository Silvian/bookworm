from django.apps import AppConfig


class FileStoreConfig(AppConfig):
    name = 'file_store'
    verbose_name = 'Files and Images'

    def ready(self):
        pass
