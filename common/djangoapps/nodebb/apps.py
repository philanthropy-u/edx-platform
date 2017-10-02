from django.apps import AppConfig


class NodebbConfig(AppConfig):
    name = u'nodebb'

    def ready(self):
        """
        Connect signal handlers.
        """
        from .signals import handlers
