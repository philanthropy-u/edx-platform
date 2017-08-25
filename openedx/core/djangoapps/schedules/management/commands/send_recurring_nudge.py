from __future__ import print_function

import datetime
import logging
import pytz
from django.contrib.sites.models import Site

from celery import task
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.http import urlquote

from openedx.core.djangoapps.schedules.models import Schedule, ScheduleConfig
from openedx.core.djangoapps.site_configuration.models import SiteConfiguration

from edx_ace.message import MessageType
from edx_ace.recipient_resolver import RecipientResolver
from edx_ace import ace
from edx_ace.recipient import Recipient


LOG = logging.getLogger(__name__)
ROUTING_KEY = getattr(settings, 'ACE_ROUTING_KEY', None)


class RecurringNudge(MessageType):
    def __init__(self, week, *args, **kwargs):
        super(RecurringNudge, self).__init__(*args, **kwargs)
        self.name = "recurringnudge_week{}".format(week)


class ScheduleStartResolver(RecipientResolver):
    def __init__(self, site, current_date):
        self.site = site
        self.current_date = current_date.replace(hour=0, minute=0, second=0)

    def send(self, week):
        """
        Send a message to all users whose schedule starts at ``self.current_date`` - ``week`` weeks.
        """
        if not ScheduleConfig.current(self.site).enqueue_recurring_nudge:
            return

        try:
            site_config = SiteConfiguration.objects.get(site_id=self.site.id)
            org_list = site_config.values.get('course_org_filter', None)
            exclude_orgs = False
            if not org_list:
                not_orgs = set()
                for other_site_config in SiteConfiguration.objects.all():
                    not_orgs.update(other_site_config.values.get('course_org_filter', []))
                org_list = list(not_orgs)
                exclude_orgs = True
            elif not isinstance(org_list, list):
                org_list = [org_list]
        except SiteConfiguration.DoesNotExist:
            org_list = None
            exclude_orgs = False

        target_date = self.current_date - datetime.timedelta(days=week * 7)
        for hour in range(24):
            target_hour = target_date + datetime.timedelta(hours=hour)
            _schedule_hour.apply_async((self.site.id, week, target_hour, org_list, exclude_orgs), retry=False)


@task(ignore_result=True, routing_key=ROUTING_KEY)
def _schedule_hour(site_id, week, target_hour, org_list, exclude_orgs=False):
    msg_type = RecurringNudge(week)

    for (user, language, context) in _schedules_for_hour(target_hour, org_list, exclude_orgs=exclude_orgs):
        msg = msg_type.personalize(
            Recipient(
                user.username,
                user.email,
            ),
            language,
            context,
        )
        _schedule_send.apply_async((site_id, msg), retry=False)


@task(ignore_result=True, routing_key=ROUTING_KEY)
def _schedule_send(site_id, msg):
    site = Site.objects.get(pk=site_id)
    if not ScheduleConfig.current(site).deliver_recurring_nudge:
        return

    ace.send(msg)


def _schedules_for_hour(target_hour, org_list, exclude_orgs=False):
    schedules = Schedule.objects.select_related(
        'enrollment__user__profile',
        'enrollment__course',
    ).filter(
        start__gte=target_hour,
        start__lt=target_hour + datetime.timedelta(minutes=60),
        enrollment__is_active=True,
    )

    if org_list is not None:
        if exclude_orgs:
            schedules = schedules.exclude(enrollment__course__org__in=org_list)
        else:
            schedules = schedules.filter(enrollment__course__org__in=org_list)

    if "read_replica" in settings.DATABASES:
        schedules = schedules.using("read_replica")

    for schedule in schedules:
        enrollment = schedule.enrollment
        user = enrollment.user

        course_id_str = str(enrollment.course_id)
        course = enrollment.course

        course_root = reverse('course_root', args=[course_id_str])

        def absolute_url(relative_path):
            return u'{}{}'.format(settings.LMS_ROOT_URL, urlquote(relative_path))

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
        parser.add_argument(
            '--date',
            default=datetime.datetime.utcnow().date().isoformat(),
            help='The date to compute weekly messages relative to, in YYYY-MM-DD format',
        )
        parser.add_argument('site_domain_name')

    def handle(self, *args, **options):
        current_date = datetime.datetime(
            *[int(x) for x in options['date'].split('-')],
            tzinfo=pytz.UTC
        )
        site = Site.objects.get(domain__iexact=options['site_domain_name'])
        resolver = ScheduleStartResolver(site, current_date)
        for week in (1, 2):
            resolver.send(week)
