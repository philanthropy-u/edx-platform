import datetime
from mock import patch, Mock
from unittest import skipUnless
import pytz

import ddt
from django.conf import settings

from opaque_keys.edx.keys import CourseKey
from openedx.core.djangoapps.schedules.management.commands import send_recurring_nudge as nudge
from openedx.core.djangoapps.site_configuration.tests.factories import SiteFactory
from openedx.core.djangolib.testing.utils import CacheIsolationTestCase
from openedx.core.djangoapps.schedules.tests.factories import ScheduleFactory, ScheduleConfigFactory
from openedx.core.djangoapps.site_configuration.tests.factories import SiteConfigurationFactory
from student.tests.factories import UserFactory


@ddt.ddt
@skipUnless('openedx.core.djangoapps.schedules.apps.SchedulesConfig' in settings.INSTALLED_APPS, "Can't test schedules if the app isn't installed")
class TestSendRecurringNudge(CacheIsolationTestCase):

    # pylint: disable=protected-access

    def setUp(self):
        ScheduleFactory.create(start=datetime.datetime(2017, 8, 1, 15, 44, 30, tzinfo=pytz.UTC))
        ScheduleFactory.create(start=datetime.datetime(2017, 8, 1, 17, 34, 30, tzinfo=pytz.UTC))
        ScheduleFactory.create(start=datetime.datetime(2017, 8, 2, 15, 34, 30, tzinfo=pytz.UTC))

        site = SiteFactory.create()
        self.site_config = SiteConfigurationFactory.create(site=site)
        ScheduleConfigFactory.create(site=self.site_config.site)

    @patch.object(nudge, 'ScheduleStartResolver')
    def test_handle(self, mock_resolver):
        test_time = datetime.datetime(2017, 8, 1, tzinfo=pytz.UTC)
        nudge.Command().handle(date='2017-08-01', site_domain_name=self.site_config.site.domain)
        mock_resolver.assert_called_with(self.site_config.site, test_time)

        for week in (1, 2):
            mock_resolver().send.assert_any_call(week)

    @patch.object(nudge, 'ace')
    @patch.object(nudge, '_schedule_hour')
    def test_resolver_send(self, mock_schedule_hour, mock_ace):
        current_time = datetime.datetime(2017, 8, 1, tzinfo=pytz.UTC)
        nudge.ScheduleStartResolver(self.site_config.site, current_time).send(3)
        test_time = current_time - datetime.timedelta(days=21)
        self.assertFalse(mock_schedule_hour.called)
        mock_schedule_hour.apply_async.assert_any_call(
            (self.site_config.site.id, 3, test_time, [], True),
            retry=False,
        )
        mock_schedule_hour.apply_async.assert_any_call(
            (self.site_config.site.id, 3, test_time + datetime.timedelta(hours=23), [], True),
            retry=False,
        )
        self.assertFalse(mock_ace.send.called)

    @ddt.data(1, 10, 100)
    @patch.object(nudge, 'ace')
    @patch.object(nudge, '_schedule_send')
    def test_schedule_hour(self, schedule_count, mock_schedule_send, mock_ace):
        schedules = [
            ScheduleFactory.create(start=datetime.datetime(2017, 8, 1, 18, 34, 30, tzinfo=pytz.UTC))
            for _ in range(schedule_count)
        ]

        test_time = datetime.datetime(2017, 8, 1, 18, tzinfo=pytz.UTC)
        with self.assertNumQueries(1):
            nudge._schedule_hour(self.site_config.site, 3, test_time, [schedules[0].enrollment.course.org])
        self.assertEqual(mock_schedule_send.apply_async.call_count, schedule_count)
        self.assertFalse(mock_ace.send.called)

    @patch.object(nudge, 'ace')
    def test_schedule_send(self, mock_ace):
        mock_msg = Mock()
        nudge._schedule_send(self.site_config.site.id, mock_msg)
        mock_ace.send.assert_called_exactly_once(mock_msg)

    @patch.object(nudge, '_schedule_send')
    def test_no_course_overview(self, mock_schedule_send):

        schedule = ScheduleFactory.create(
            start=datetime.datetime(2017, 8, 1, 20, 34, 30, tzinfo=pytz.UTC),
        )
        schedule.enrollment.course_id = CourseKey.from_string('edX/toy/Not_2012_Fall')
        schedule.enrollment.save()

        test_time = datetime.datetime(2017, 8, 1, 20, tzinfo=pytz.UTC)
        with self.assertNumQueries(1):
            nudge._schedule_hour(self.site_config.site, 3, test_time, [schedule.enrollment.course.org])

        # There is no database constraint that enforces that enrollment.course_id points
        # to a valid CourseOverview object. However, in that case, schedules isn't going
        # to attempt to address it, and will instead simply skip those users.
        # This happens 'transparently' because django generates an inner-join between
        # enrollment and course_overview, and thus will skip any rows where course_overview
        # is null.
        self.assertEqual(mock_schedule_send.apply_async.call_count, 0)

    @patch.object(nudge, 'ace')
    def test_delivery_disabled(self, mock_ace):
        ScheduleConfigFactory.create(site=self.site_config.site, deliver_recurring_nudge=False)

        mock_msg = Mock()
        nudge._schedule_send(self.site_config.site.id, mock_msg)
        self.assertFalse(mock_ace.send.called)

    @patch.object(nudge, 'ace')
    @patch.object(nudge, '_schedule_hour')
    def test_enqueue_disabled(self, mock_schedule_hour, mock_ace):
        ScheduleConfigFactory.create(site=self.site_config.site, enqueue_recurring_nudge=False)

        current_time = datetime.datetime(2017, 8, 1, tzinfo=pytz.UTC)
        nudge.ScheduleStartResolver(self.site_config.site, current_time).send(3)
        self.assertFalse(mock_schedule_hour.called)
        self.assertFalse(mock_schedule_hour.apply_async.called)
        self.assertFalse(mock_ace.send.called)

    @patch.object(nudge, 'ace')
    @patch.object(nudge, '_schedule_send')
    @ddt.data(
        ((['filtered_org'], False, 1)),
        ((['filtered_org'], True, 2))
    )
    @ddt.unpack
    def test_site_config(self, org_list, exclude_orgs, expected_message_count, mock_schedule_send, mock_ace):
        filtered_org = 'filtered_org'
        unfiltered_org = 'unfiltered_org'
        site1 = SiteFactory.create(domain='foo1.bar', name='foo1.bar')
        limited_config = SiteConfigurationFactory.create(values={'course_org_filter': [filtered_org]}, site=site1)
        site2 = SiteFactory.create(domain='foo2.bar', name='foo2.bar')
        unlimited_config = SiteConfigurationFactory.create(values={'course_org_filter': []}, site=site2)

        for config in (limited_config, unlimited_config):
            ScheduleConfigFactory.create(site=config.site)

        filtered_sched = ScheduleFactory.create(
            start=datetime.datetime(2017, 8, 2, 17, 44, 30, tzinfo=pytz.UTC),
            enrollment__course__org=filtered_org,
        )
        unfiltered_scheds = [
            ScheduleFactory.create(
                start=datetime.datetime(2017, 8, 2, 17, 44, 30, tzinfo=pytz.UTC),
                enrollment__course__org=unfiltered_org,
            )
            for _ in range(2)
        ]

        print(filtered_sched.enrollment)
        print(filtered_sched.enrollment.course)
        print(filtered_sched.enrollment.course.org)
        print(unfiltered_scheds[0].enrollment)
        print(unfiltered_scheds[0].enrollment.course)
        print(unfiltered_scheds[0].enrollment.course.org)
        print(unfiltered_scheds[1].enrollment)
        print(unfiltered_scheds[1].enrollment.course)
        print(unfiltered_scheds[1].enrollment.course.org)

        test_time = datetime.datetime(2017, 8, 2, 17, tzinfo=pytz.UTC)
        with self.assertNumQueries(1):
            nudge._schedule_hour(limited_config.site.id, 3, test_time, org_list=org_list, exclude_orgs=exclude_orgs)

        print(mock_schedule_send.mock_calls)
        self.assertEqual(mock_schedule_send.apply_async.call_count, expected_message_count)
        self.assertFalse(mock_ace.send.called)
