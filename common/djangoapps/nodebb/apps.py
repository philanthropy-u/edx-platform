from django.apps import AppConfig


class NodebbConfig(AppConfig):
    name = u'nodebb'

    def ready(self):
        """
        Connect signal handlers.
        """
        from nodebb.signals.handlers import create_category_on_nodebb, join_group_on_nodebb
