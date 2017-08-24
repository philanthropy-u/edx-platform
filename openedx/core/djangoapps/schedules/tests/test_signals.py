from django.test import TestCase
from mock import patch

from openedx.core.djangoapps.schedules.signals import SCHEDULE_WAFFLE_FLAG
from openedx.core.djangoapps.site_configuration.tests.factories import SiteFactory
from openedx.core.djangoapps.waffle_utils.testutils import override_waffle_flag
from openedx.core.djangolib.testing.utils import skip_unless_lms
from student.tests.factories import CourseEnrollmentFactory
from ..models import Schedule
from ..tests.factories import ScheduleConfigFactory


@patch('openedx.core.djangoapps.schedules.signals.get_current_site')
@skip_unless_lms
class CreateScheduleTests(TestCase):

    def assert_schedule_created(self):
        enrollment = CourseEnrollmentFactory()
        self.assertIsNotNone(enrollment.schedule)

    def assert_schedule_not_created(self):
        enrollment = CourseEnrollmentFactory()
        with self.assertRaises(Schedule.DoesNotExist):
            enrollment.schedule

    @override_waffle_flag(SCHEDULE_WAFFLE_FLAG, True)
    def test_create_schedule(self, mock_get_current_site):
        site = SiteFactory.create()
        mock_get_current_site.return_value = site
        ScheduleConfigFactory.create(site=site, enabled=True)
        self.assert_schedule_created()

    @override_waffle_flag(SCHEDULE_WAFFLE_FLAG, True)
    def test_no_current_site(self, mock_get_current_site):
        mock_get_current_site.return_value = None
        self.assert_schedule_not_created()

    @override_waffle_flag(SCHEDULE_WAFFLE_FLAG, True)
    def test_schedule_config_disabled_waffle_enabled(self, mock_get_current_site):
        site = SiteFactory.create()
        mock_get_current_site.return_value = site
        ScheduleConfigFactory.create(site=site, enabled=False)
        self.assert_schedule_created()

    @override_waffle_flag(SCHEDULE_WAFFLE_FLAG, False)
    def test_schedule_config_enabled_waffle_disabled(self, mock_get_current_site):
        site = SiteFactory.create()
        mock_get_current_site.return_value = site
        ScheduleConfigFactory.create(site=site, enabled=True)
        self.assert_schedule_created()

    @override_waffle_flag(SCHEDULE_WAFFLE_FLAG, False)
    def test_schedule_config_disabled_waffle_disabled(self, mock_get_current_site):
        site = SiteFactory.create()
        mock_get_current_site.return_value = site
        ScheduleConfigFactory.create(site=site, enabled=False)
        self.assert_schedule_not_created()
