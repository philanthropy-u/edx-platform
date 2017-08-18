"""
Schedule related signal handlers.
"""
import datetime
import logging

from django.dispatch import receiver
from django.utils import timezone

from openedx.core.djangoapps.schedules.models import Schedule, ScheduleConfig
from openedx.core.djangoapps.waffle_utils import CourseWaffleFlag
from student.models import ENROLL_STATUS_CHANGE, EnrollStatusChange, CourseEnrollment

log = logging.getLogger(__name__)


SCHEDULE_WAFFLE_SWITCHES = CourseWaffleFlag(
    waffle_namespace='schedules',
    flag_name='create_schedules_for_course',
    flag_undefined_default=False
)


@receiver(ENROLL_STATUS_CHANGE)
def create_schedule_for_self_paced_enrollment(sender, event=None, user=None, course_id=None, **kwargs):
    log.info('Running schedule signal handler')
    if event != EnrollStatusChange.enroll:
        return

    if not (
        ScheduleConfig.current().is_enabled or
        SCHEDULE_WAFFLE_SWITCHES.is_enabled(course_id)
    ):
        return

    log.info('Creating schedule for new enrollment')
    enrollment = CourseEnrollment.get_enrollment(user, course_id)
    schedule = Schedule(
        enrollment=enrollment,
        active=True,
        start=timezone.now(),
        upgrade_deadline=timezone.now() + datetime.timedelta(days=21)
    )
    schedule.save()
