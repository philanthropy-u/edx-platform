from django.core.management.base import BaseCommand
from django.db import close_old_connections


class Command(BaseCommand):

    def handle(self, *args, **options):
        close_old_connections()
