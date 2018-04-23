from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = 'authentication'
    verbose_name = 'User Authentication'

    def ready(self):
        from authentication import models_circles  # noqa
        from authentication import signals  # noqa
