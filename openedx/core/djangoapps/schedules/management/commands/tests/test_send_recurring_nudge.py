import datetime
from mock import patch, Mock
from unittest import skipUnless
import pytz

import ddt
from django.conf import settings

from opaque_keys.edx.keys import CourseKey
from openedx.core.djangoapps.schedules.management.commands import send_recurring_nudge as nudge
from openedx.core.djangolib.testing.utils import CacheIsolationTestCase
from openedx.core.djangoapps.schedules.tests.factories import ScheduleFactory
from student.tests.factories import UserFactory


@ddt.ddt
@skipUnless('openedx.core.djangoapps.schedules.apps.SchedulesConfig' in settings.INSTALLED_APPS, "Can't test schedules if the app isn't installed")
class TestSendRecurringNudge(CacheIsolationTestCase):

    # pylint: disable=protected-access

    def setUp(self):
        ScheduleFactory.create(start=datetime.datetime(2017, 8, 1, 15, 44, 30, tzinfo=pytz.UTC))
        ScheduleFactory.create(start=datetime.datetime(2017, 8, 1, 17, 34, 30, tzinfo=pytz.UTC))
        ScheduleFactory.create(start=datetime.datetime(2017, 8, 2, 15, 34, 30, tzinfo=pytz.UTC))

    @patch.object(nudge, 'ScheduleStartResolver')
    def test_handle(self, mock_resolver):
        test_time = datetime.datetime(2017, 8, 1, tzinfo=pytz.UTC)
        nudge.Command().handle(date='2017-08-01')
        mock_resolver.assert_called_with(test_time)

        for week in (1, 2):
            mock_resolver().send.assert_any_call(week)

    @patch.object(nudge, 'ace')
    @patch.object(nudge, '_schedule_hour')
    def test_resolver_send(self, mock_schedule_hour, mock_ace):
        current_time = datetime.datetime(2017, 8, 1, tzinfo=pytz.UTC)
        nudge.ScheduleStartResolver(current_time).send(3)
        test_time = current_time - datetime.timedelta(days=21)
        self.assertFalse(mock_schedule_hour.called)
        mock_schedule_hour.delay.assert_any_call(3, test_time)
        mock_schedule_hour.delay.assert_any_call(3, test_time + datetime.timedelta(hours=23))
        self.assertFalse(mock_ace.send.called)

    @ddt.data(1, 10, 100)
    @patch.object(nudge, 'ace')
    @patch.object(nudge, '_schedule_send')
    def test_schedule_hour(self, schedule_count, mock_schedule_send, mock_ace):
        for _ in range(schedule_count):
            ScheduleFactory.create(start=datetime.datetime(2017, 8, 1, 18, 34, 30, tzinfo=pytz.UTC))

        test_time = datetime.datetime(2017, 8, 1, 18, tzinfo=pytz.UTC)
        with self.assertNumQueries(1):
            nudge._schedule_hour(3, test_time)
        self.assertEqual(mock_schedule_send.delay.call_count, schedule_count)
        self.assertFalse(mock_ace.send.called)

    @patch.object(nudge, 'ace')
    def test_schedule_send(self, mock_ace):
        mock_msg = Mock()
        nudge._schedule_send(mock_msg)
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
            nudge._schedule_hour(3, test_time)

        # There is no database constraint that enforces that enrollment.course_id points
        # to a valid CourseOverview object. However, in that case, schedules isn't going
        # to attempt to address it, and will instead simply skip those users.
        # This happens 'transparently' because django generates an inner-join between
        # enrollment and course_overview, and thus will skip any rows where course_overview
        # is null.
        self.assertEqual(mock_schedule_send.delay.call_count, 0)
