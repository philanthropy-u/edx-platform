from __future__ import print_function

import datetime
import logging
import pytz

from celery import task
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.urlresolvers import reverse

from openedx.core.djangoapps.schedules.models import Schedule

from edx_ace.message import MessageType
from edx_ace.recipient_resolver import RecipientResolver
from edx_ace import ace
from edx_ace.recipient import Recipient


LOG = logging.getLogger(__name__)


class RecurringNudge(MessageType):
    def __init__(self, week, *args, **kwargs):
        super(RecurringNudge, self).__init__(*args, **kwargs)
        self.name = "recurringnudge_week{}".format(week)


class ScheduleStartResolver(RecipientResolver):
    def __init__(self, current_date):
        self.current_date = current_date.replace(hour=0, minute=0, second=0)

    def send(self, week):
        target_date = self.current_date - datetime.timedelta(days=week * 7)
        for hour in range(24):
            target_hour = target_date + datetime.timedelta(hours=hour)
            _schedule_hour.delay(week, target_hour)


@task(ignore_result=True, routing_key=settings.ACE_ROUTING_KEY)
def _schedule_hour(week, target_hour):
    msg_type = RecurringNudge(week)

    for (user, language, context) in _schedules_for_hour(target_hour):
        msg = msg_type.personalize(
            Recipient(
                user.username,
                user.email,
            ),
            language,
            context,
        )
        # TODO: what do we do about failed send tasks?
        _schedule_send.delay(msg)


@task(ignore_result=True, routing_key=settings.ACE_ROUTING_KEY)
def _schedule_send(msg):
    try:
        ace.send(msg)
    except Exception:
        LOG.exception('Unable to queue message %s', msg)
        raise


def _schedules_for_hour(target_hour):
    schedules = Schedule.objects.select_related(
        'enrollment__user__profile',
        'enrollment__course',
    ).filter(
        start__gte=target_hour,
        start__lt=target_hour + datetime.timedelta(minutes=60),
    )

    if "read_replica" in settings.DATABASES:
        schedules = schedules.using("read_replica")

    for schedule in schedules:
        enrollment = schedule.enrollment
        user = enrollment.user

        course_id_str = str(enrollment.course_id)
        course = enrollment.course

        # TODO: this produces a URL that contains the literal "+" character in the course key, which breaks sailthru
        course_root = reverse('course_root', kwargs={'course_id': course_id_str})

        def absolute_url(relative_path):
            return u'{}{}'.format(settings.LMS_ROOT_URL, relative_path)

        template_context = {
            'student_name': user.profile.name,
            'course_name': course.display_name,
            'course_url': absolute_url(course_root),

            # This is used by the bulk email optout policy
            'course_id': course_id_str,
        }

        yield (user, course.language, template_context)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--date', default=datetime.datetime.utcnow().date().isoformat())

    def handle(self, *args, **options):
        current_date = datetime.datetime(
            *[int(x) for x in options['date'].split('-')],
            tzinfo=pytz.UTC
        )
        resolver = ScheduleStartResolver(current_date)
        for week in (1, 2):
            resolver.send(week)
