import json

from mock import patch
from pytz import UTC
from dateutil.parser import parse
from datetime import datetime
from django.test import override_settings

from . import helpers as test_helpers
from cms.djangoapps.contentstore.tests.utils import CourseTestCase
from cms.djangoapps.contentstore.tasks import rerun_course as rerun_course_task
from course_action_state.models import CourseRerunState
from lms.djangoapps.courseware.courses import get_course_by_id
from openedx.features.cms import helpers
from opaque_keys.edx.locator import CourseLocator
from openassessment.xblock.defaults import DEFAULT_START, DEFAULT_DUE
from xmodule.modulestore.tests.factories import CourseFactory
from xmodule.modulestore import EdxJSONEncoder
from xmodule.course_module import CourseFields


class CourseRerunAutomationTestCase(CourseTestCase):
    """
    Class for test cases related to course re-run (course automation, in general)
    """

    def setUp(self):
        super(CourseRerunAutomationTestCase, self).setUp()
        # create source course
        self.source_course = test_helpers.create_source_course(self.store, self.user,
                                                               datetime(2019, 9, 1, tzinfo=UTC))

    @patch('openedx.features.cms.helpers.set_rerun_course_dates')
    @patch('openedx.features.cms.helpers.initialize_course_settings')
    def test_apply_post_rerun_creation_tasks_with_new_course_start_date(
            self, mock_set_rerun_course_dates, mock_initialize_course_settings):
        """
        Testing apply_post_rerun_creation_tasks method if course start date is valid and not
        default course start date
        """
        dest_course = CourseFactory.create(
            org='origin',
            number='the_beginning_22',
            run='second_test_2',
            display_name='destination course',
            start=datetime(2018, 8, 1, tzinfo=UTC)
        )
        helpers.apply_post_rerun_creation_tasks(self.source_course.id, dest_course.id, self.user.id)
        assert mock_initialize_course_settings.called
        assert mock_set_rerun_course_dates.called

    @patch('openedx.features.cms.helpers.set_rerun_course_dates')
    @patch('openedx.features.cms.helpers.initialize_course_settings')
    def test_apply_post_rerun_creation_tasks_with_default_course_start_date(
            self, mock_initialize_course_settings, mock_set_rerun_course_dates):
        """
        Testing apply_post_rerun_creation_tasks method if course start date is default date
        """
        dest_course_default_date = CourseFactory.create(
            org='origin',
            number='the_beginning_2',
            run='second_test_2',
            display_name='destination course',
            start=CourseFields.start.default
        )
        helpers.apply_post_rerun_creation_tasks(self.source_course.id, dest_course_default_date.id,
                                                self.user.id)
        assert mock_initialize_course_settings.called
        assert not mock_set_rerun_course_dates.called

    @patch('openedx.features.cms.helpers.set_rerun_ora_dates')
    @patch('openedx.features.cms.helpers.set_rerun_module_dates')
    @patch('openedx.features.cms.helpers.set_advanced_settings_due_date')
    @patch('openedx.features.cms.helpers.set_rerun_schedule_dates')
    def test_set_rerun_course_dates_with_load_factor(self, mock_set_rerun_schedule_dates,
                                                     mock_set_advanced_settings_due_date,
                                                     mock_set_rerun_module_dates,
                                                     mock_set_rerun_ora_dates):
        """
        Testing set_rerun_course_dates method with a source course having few children up to the
        level of component
        """
        source_courses = test_helpers.create_large_course(self.store, 2,
                                                          datetime(2019, 4, 1, tzinfo=UTC))
        rerun_courses = test_helpers.create_large_course(self.store, 2,
                                                         datetime(2019, 4, 1, tzinfo=UTC))
        source_courses[0].start = datetime(2019, 5, 1, tzinfo=UTC)

        source_course = get_course_by_id(source_courses[0].id)
        rerun_course = get_course_by_id(rerun_courses[0].id)

        helpers.set_rerun_course_dates(source_course, rerun_course, self.user.id)
        assert mock_set_rerun_schedule_dates.called
        assert mock_set_advanced_settings_due_date.called
        assert mock_set_rerun_module_dates.called
        assert mock_set_rerun_ora_dates.called

    @patch('openedx.features.cms.helpers.set_rerun_ora_dates')
    @patch('openedx.features.cms.helpers.set_rerun_module_dates')
    @patch('openedx.features.cms.helpers.set_advanced_settings_due_date')
    @patch('openedx.features.cms.helpers.set_rerun_schedule_dates')
    def test_set_rerun_course_dates_with_empty_course(self, mock_set_rerun_schedule_dates,
                                                      mock_set_advanced_settings_due_date,
                                                      mock_set_rerun_module_dates,
                                                      mock_set_rerun_ora_dates):
        """
        Testing set_rerun_course_dates method with empty source course
        """
        source_course = CourseFactory.create(
            modulestore=self.store,
            start=datetime(2019, 4, 1, tzinfo=UTC)
        )
        rerun_course = CourseFactory.create(
            modulestore=self.store,
            start=datetime(2019, 5, 1, tzinfo=UTC)
        )
        helpers.set_rerun_course_dates(source_course, rerun_course, self.user.id)

        assert not mock_set_rerun_schedule_dates.called
        assert not mock_set_advanced_settings_due_date.called
        assert not mock_set_rerun_module_dates.called
        assert not mock_set_rerun_ora_dates.called

    @override_settings(
        CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
        CELERY_ALWAYS_EAGER=True,
        BROKER_BACKEND='memory'
    )
    @patch('cms.djangoapps.contentstore.tasks.apply_post_rerun_creation_tasks')
    def test_set_rerun_module_dates(self, mock_apply_post_rerun_creation_tasks):
        """
        Testing start date of chapters (sequence) and start & due date of sub-sequences
        (sequential) by creating a re-run of source course
        """

        mock_apply_post_rerun_creation_tasks.return_value = None

        # Creating re-run for source course

        rerun_course_id = CourseLocator(
            org="edx3", course="split3", run="rerun_test"
        )
        # Mark the action as initiated
        fields = {'display_name': 'rerun', "start": "2019-10-01T00:00:00Z"}
        CourseRerunState.objects.initiated(self.source_course.id, rerun_course_id, self.user,
                                           fields['display_name'])

        result = rerun_course_task.delay(unicode(self.source_course.id), unicode(rerun_course_id),
                                         self.user.id, json.dumps(fields, cls=EdxJSONEncoder))
        self.assertEqual(result.get(), "succeeded")

        # Re-run from source course complete
        # Testing start date of chapters (sequence)
        # Testing start and due date of sub-sequences (sequential)

        rerun_course = get_course_by_id(rerun_course_id)
        source_course_start_date = self.source_course.start
        re_run_start_date = rerun_course.start

        self.assertEqual(re_run_start_date, datetime(2019, 10, 1, tzinfo=UTC))

        source_course_sections = self.source_course.get_children()
        source_course_subsections = [sub_section for s in source_course_sections for sub_section in
                                     s.get_children()]
        re_run_sections = rerun_course.get_children()
        re_run_subsections = [sub_section for s in re_run_sections for sub_section in
                              s.get_children()]

        # If there are no sections ignore setting dates
        if not re_run_sections:
            return

        re_run_modules = re_run_sections + re_run_subsections
        source_course_modules = source_course_sections + source_course_subsections

        helpers.set_rerun_module_dates(re_run_modules, source_course_modules,
                                       source_course_start_date,
                                       re_run_start_date, self.user)

        rerun_course = get_course_by_id(rerun_course_id)

        # chapter 1 (section)
        chapter1 = rerun_course.get_children()[0]
        self.assertEqual(chapter1.start, datetime(2019, 10, 1, tzinfo=UTC))
        # chapter (section) does not have due dates, so it must be None
        self.assertIsNone(chapter1.due)
        self.assertEqual(len(chapter1.get_children()), 1)

        # chapter 1, sequential 1 (sub-section)
        chapter1_sequential = chapter1.get_children()[0]
        self.assertEqual(chapter1_sequential.start, datetime(2019, 10, 1, tzinfo=UTC))
        # Due date we not set in source course, hence re-run course must not have it
        self.assertIsNone(chapter1_sequential.due)

        # chapter 2 (section)
        chapter2 = rerun_course.get_children()[1]
        self.assertEqual(chapter2.start, datetime(2019, 10, 31, tzinfo=UTC))
        # chapter (section) does not have due dates, so it must be None
        self.assertIsNone(chapter2.due)
        self.assertEqual(len(chapter2.get_children()), 2)

        chapter2_sequential1 = chapter2.get_children()[0]
        self.assertEqual(chapter2_sequential1.start, datetime(2019, 11, 9, tzinfo=UTC))
        self.assertEqual(chapter2_sequential1.due, datetime(2019, 11, 19, tzinfo=UTC))

        chapter2_sequential2 = chapter2.get_children()[1]
        self.assertEqual(chapter2_sequential2.start, datetime(2019, 12, 1, tzinfo=UTC))
        self.assertIsNone(chapter2_sequential2.due)

        # chapter 3 (section)
        chapter3 = rerun_course.get_children()[2]
        self.assertEqual(chapter3.start, datetime(2019, 12, 1, tzinfo=UTC))
        # chapter (section) does not have due dates, so it must be None
        self.assertIsNone(chapter3.due)
        # This chapter was empty
        self.assertFalse(chapter3.get_children())

    def test_calculate_date_by_delta_near_future(self):
        """
        Testing near future date by adding delta into it
        """
        date_to_update = datetime(2019, 9, 15, tzinfo=UTC)
        # delta is be 31 days
        source_course_start_date = datetime(2019, 1, 1, tzinfo=UTC)
        re_run_course_start_date = datetime(2019, 2, 1, tzinfo=UTC)

        result = helpers.calculate_date_by_delta(date_to_update, source_course_start_date,
                                                 re_run_course_start_date)
        self.assertEqual(result, datetime(2019, 10, 16, tzinfo=UTC))

    def test_calculate_date_by_delta_past(self):
        """
        Testing past date by adding delta into it
        """
        date_to_update = datetime(2019, 9, 15, tzinfo=UTC)
        # delta is be (-ive) 16 years 8 months 17 days
        source_course_start_date = datetime(2019, 1, 1, tzinfo=UTC)
        re_run_course_start_date = datetime(2002, 4, 15, tzinfo=UTC)

        result = helpers.calculate_date_by_delta(date_to_update, source_course_start_date,
                                                 re_run_course_start_date)
        # Manually calculated date is 1 day less than actual date
        self.assertEqual(result, datetime(2002, 12, 28, tzinfo=UTC))

    def test_calculate_date_by_delta_future(self):
        """
        Testing future date by adding delta into it
        """
        date_to_update = datetime(2019, 9, 15, tzinfo=UTC)
        # delta is be (-ive) 9 years 3 months 14 days
        source_course_start_date = datetime(2019, 1, 1, tzinfo=UTC)
        re_run_course_start_date = datetime(2028, 4, 15, tzinfo=UTC)

        result = helpers.calculate_date_by_delta(date_to_update, source_course_start_date,
                                                 re_run_course_start_date)
        self.assertEqual(result, datetime(2028, 12, 28, tzinfo=UTC))

    def test_component_update_successful(self):
        """
        Testing updating component in store
        """
        courses = test_helpers.create_large_course(self.store, 1)
        components = self.store.get_items(
            courses[0].id,
            qualifiers={'category': 'html'}
        )

        # change title of component and update it via module store
        components[0].display_name = "Testing HTML"
        helpers.component_update(components[0], self.user)

        # Find component which is updated and get display name for testing
        updated_components = self.store.get_items(
            courses[0].id,
            qualifiers={'category': 'html'}
        )

        # since load factor was one, there should be only one html component
        self.assertEqual(len(updated_components), 1)
        self.assertEqual(updated_components[0].display_name, "Testing HTML")

    def test_set_rerun_ora_dates(self):
        """
        Testing all dates in ORA. In our case self.source_course can server the purpose of
        rerun_course, so we can consider source_course as rerun_course
        """
        # ORA dates will be updated by +ive 30 day
        source_course_start_date = datetime(2019, 9, 1, tzinfo=UTC)
        re_run_start_date = datetime(2019, 10, 1, tzinfo=UTC)

        re_run_sections = self.source_course.get_children()
        re_run_subsections = [sub_section for s in re_run_sections for sub_section in
                              s.get_children()]

        helpers.set_rerun_ora_dates(re_run_subsections, re_run_start_date, source_course_start_date,
                                    self.user)

        # Get updated ORA components from store
        ora_list_in_course = self.store.get_items(
            self.source_course.id,
            qualifiers={'category': 'openassessment'}
        )

        # course course had only two ORA components, re-run course must have same count
        self.assertEqual(len(ora_list_in_course), 2)

        ora1 = ora_list_in_course[0]
        ora2 = ora_list_in_course[1]

        # assertions for ORA - default assessment dates

        self.assertEqual(ora1.display_name, "ORA - default assessment dates")
        self.assertEqual(parse(ora1.submission_start), datetime(2019, 1, 31, tzinfo=UTC))
        self.assertEqual(parse(ora1.submission_due), datetime(2019, 3, 3, tzinfo=UTC))

        ora1_student_training = ora1.rubric_assessments[0]
        self.assertIsNone(ora1_student_training['start'])
        self.assertIsNone(ora1_student_training['due'])
        self.assertEqual(ora1_student_training['name'], 'student-training')

        date_default_start = parse(DEFAULT_START)
        date_default_end = parse(DEFAULT_DUE)

        # peer, self and staff assessment all have default date so, their dates must not change
        iter_assessment = iter(ora1.rubric_assessments)
        next(iter_assessment)
        for assessment in iter_assessment:
            self.assertEqual(parse(assessment['start']), date_default_start)
            self.assertEqual(parse(assessment['due']), date_default_end)

        # assertions for ORA - all custom dates

        self.assertEqual(ora2.display_name, "ORA - all custom dates")
        self.assertEqual(parse(ora2.submission_start), datetime(2019, 1, 31, tzinfo=UTC))
        self.assertEqual(parse(ora2.submission_due), datetime(2019, 3, 3, tzinfo=UTC))

        ora2_student_training = ora2.rubric_assessments[0]
        self.assertIsNone(ora2_student_training['start'])
        self.assertIsNone(ora2_student_training['due'])
        self.assertEqual(ora2_student_training['name'], 'student-training')

        ora2_peer_assessment = ora2.rubric_assessments[1]
        # providing dates without time zone info
        self.assertEqual(parse(ora2_peer_assessment['start']), datetime(2019, 3, 31, tzinfo=UTC))
        self.assertEqual(parse(ora2_peer_assessment['due']), datetime(2019, 5, 1, tzinfo=UTC))

        ora2_self_assessment = ora2.rubric_assessments[2]
        self.assertEqual(parse(ora2_self_assessment['start']), datetime(2019, 5, 31, tzinfo=UTC))
        self.assertEqual(parse(ora2_self_assessment['due']), datetime(2019, 7, 1, tzinfo=UTC))

        ora2_staff_assessment = ora2.rubric_assessments[3]
        self.assertEqual(parse(ora2_staff_assessment['start']), datetime(2019, 7, 31, tzinfo=UTC))
        self.assertEqual(parse(ora2_staff_assessment['due']), datetime(2019, 8, 31, tzinfo=UTC))

    def tearDown(self):
        super(CourseRerunAutomationTestCase, self).tearDown()
