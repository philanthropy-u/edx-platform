from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from edx_notifications import startup
from edx_notifications.data import NotificationType
from edx_notifications.lib.publisher import register_notification_type
from edx_notifications.signals import perform_type_registrations
from nodebb.tasks import task_delete_badge_info_from_nodebb, task_sync_badge_info_with_nodebb

from .constants import PHILU_BADGING_NOTIFICATION_RENDERER, PHILU_BADGING_NOTIFICATION_TYPE
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


@receiver(startup.perform_type_registrations)
def register_notification_types(sender, **kwargs):  # pylint: disable=unused-argument
    """
    Register philu NotificationTypes.
    This will be called automatically on the Notification subsystem startup (because we are
    receiving the 'perform_type_registrations' signal)
    """
    register_notification_type(
            NotificationType(
                name=PHILU_BADGING_NOTIFICATION_TYPE.format(prefix='philu.badging', type='user-badge-earned'),
                renderer=PHILU_BADGING_NOTIFICATION_RENDERER,
            )
        )
