from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save

from common.djangoapps.nodebb.tasks import task_sync_badge_info_with_nodebb, task_delete_badge_info_with_nodebb
from .models import Badge


@receiver(post_save, sender=Badge)
def sync_badge_info_with_nodebb(sender, instance, update_fields, **kwargs):
    task_sync_badge_info_with_nodebb.delay(instance)


@receiver(post_delete, sender=Badge)
def delete_badge_info_with_nodebb(sender, instance, update_fields, **kwargs):
    task_delete_badge_info_with_nodebb.delay(instance)
