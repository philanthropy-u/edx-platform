from logging import getLogger

from django.db.models.signals import post_save
from django.dispatch import receiver

from nodebb.tasks import create_category_on_nodebb_task, join_group_on_nodebb_task
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from student.models import ENROLL_STATUS_CHANGE, EnrollStatusChange
from xmodule.modulestore.django import modulestore

log = getLogger(__name__)


@receiver(post_save, sender=CourseOverview, dispatch_uid="nodebb.signals.handlers.create_category_on_nodebb")
def create_category_on_nodebb(sender, instance, created, **kwargs):
    if created:
        # Start a celery task to create a community on node bb
        create_category_on_nodebb_task.delay(instance.display_name)


@receiver(ENROLL_STATUS_CHANGE)
def join_group_on_nodebb(sender, event=None, user=None, **kwargs):  # pylint: disable=unused-argument
    if event == EnrollStatusChange.enroll:
        course = modulestore().get_course(kwargs.get('course_id'))

        # Start a celery task to add a user in the group on node bb
        join_group_on_nodebb_task.delay(user.username, course.display_name)
