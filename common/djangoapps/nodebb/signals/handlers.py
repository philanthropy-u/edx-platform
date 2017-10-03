from logging import getLogger

from django.db.models.signals import post_save
from django.dispatch import receiver

from lms.lib.nodebb_client.client import NodeBBClient
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from xmodule.modulestore.django import modulestore

log = getLogger(__name__)


@receiver(post_save, sender=CourseOverview)
def create_category_on_nodebb(sender, instance, created, **kwargs):
    if created:
        course_data = modulestore().get_course(instance.id)
        user_id = course_data._edited_by

        status_code, response_body = NodeBBClient().categories.create(name=instance.display_name)

        if status_code != 200:
            log.error(
                'Cant create community for the given course {} due to {}'.format(instance.course_id, response_body)
            )

        log.info('Community created for course {}'.format(instance.course_id))
