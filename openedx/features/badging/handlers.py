from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from nodebb.tasks import task_delete_badge_info_from_nodebb, task_sync_badge_info_with_nodebb

from .models import Badge


@receiver(post_save, sender=Badge)
def sync_badge_info_with_nodebb(sender, instance, update_fields, **kwargs):
    """When badge is created or updated in platform, sync it in NodeBB."""
    badge_info = {
        'id': instance.id,
        'name': instance.name,
        'type': instance.type,
        'threshold': instance.threshold,
        'image': instance.image
    }
    task_sync_badge_info_with_nodebb.delay(badge_info)


@receiver(post_delete, sender=Badge)
def delete_badge_info_from_nodebb(sender, instance, **kwargs):
    """On badge deletion, delete it from NodeBB. This will not effect any post count on NodeBB."""
    badge_data = {
        'id': instance.id
    }
    task_delete_badge_info_from_nodebb.delay(badge_data)
