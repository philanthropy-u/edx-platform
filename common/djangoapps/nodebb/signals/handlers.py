from logging import getLogger

from django.db.models.signals import post_save
from django.dispatch import receiver

from lms.lib.nodebb_client.client import NodeBBClient
from xmodule.modulestore.django import modulestore
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from student.models import CourseEnrollment

log = getLogger(__name__)


@receiver(post_save, sender=CourseOverview, dispatch_uid="nodebb.signals.handlers.create_category_on_nodebb")
def create_category_on_nodebb(sender, instance, created, **kwargs):
    if created:
        status_code, response_body = NodeBBClient().categories.create(name=instance.display_name)

        if status_code != 200:
            log.error(
                'Cant create community for the given course {} due to {}'.format(instance.id, response_body)
            )

        log.info('Community created for course {}'.format(instance.id))


@receiver(post_save, sender=CourseEnrollment, dispatch_uid="nodebb.signals.handlers.join_group_on_nodebb")
def join_group_on_nodebb(sender, instance, created, **kwargs):
    if created:
        user_name = instance.user.username
        course = modulestore().get_course(instance.course_id)
        status_code, response_body = NodeBBClient().users.join(group_name=course.display_name,
                                                               user_name=user_name)

        if status_code != 200:
            log.error(
                'Can not join the group {} due to {}'.format(course.display_name, response_body)
            )

        log.info('User have joined the group {} successfully'.format(course.display_name))
