from crum import set_current_request
from datetime import timedelta
from django.test.client import RequestFactory

from course_action_state.models import CourseRerunState
from custom_settings.models import CustomSettings
from xmodule.modulestore import ModuleStoreEnum
from xmodule.modulestore.tests.factories import CourseFactory

from .test_views import CourseCardBaseClass
from ..helpers import *
from ..models import CourseCard


class CourseCardHelperBaseClass(CourseCardBaseClass):

    def setUp(self):
        super(CourseCardHelperBaseClass, self).setUp()

        self.rerun_parent_course = self.courses[0]
        org = self.rerun_parent_course.org
        course_number = self.rerun_parent_course.number
        course_run = '2015_Q2'
        display_name = self.rerun_parent_course.display_name + ' - re run'

        self.re_run_course = CourseFactory.create(org=org, number=course_number, run=course_run,
                                                  display_name=display_name, default_store=ModuleStoreEnum.Type.split)

        CourseRerunState.objects.initiated(self.rerun_parent_course.id, self.re_run_course.id, self.staff,
                                           display_name=display_name)

    def test_get_related_card_id(self):
        non_re_run_course_id = self.courses[1].id
        parent_course_id = self.rerun_parent_course.id
        re_run_course_id = self.re_run_course.id

        # Desired output is the parent's course id
        self.assertEqual(get_related_card_id(re_run_course_id), parent_course_id)

        # For courses without a rerun the passed course id is returned as it is
        self.assertEqual(get_related_card_id(non_re_run_course_id), non_re_run_course_id)

        # For parent course id as input, the same course id should be returned
        self.assertEqual(get_related_card_id(parent_course_id), parent_course_id)

    def test_get_related_card(self):
        non_re_run_course = self.courses[1]

        # Desired output is the parent course when course which is a rerun is passed as input
        self.assertEqual(get_related_card(self.re_run_course).id, self.rerun_parent_course.id)

        # For courses without a rerun the passed course is returned as it is
        self.assertEqual(get_related_card(non_re_run_course).id, non_re_run_course.id)

        # For parent course as input, the parent course should be returned as it is
        self.assertEqual(get_related_card(self.rerun_parent_course).id, self.rerun_parent_course.id)

    def test_get_future_courses(self):
        CourseRerunState.objects.succeeded(course_key=self.re_run_course.id)

        re_run_course_overview = CourseOverview.get_from_id(course_id=self.re_run_course.id)

        re_run_course_overview.end = datetime.utcnow() - timedelta(days=120)
        re_run_course_overview.start = datetime.utcnow() - timedelta(days=150)
        re_run_course_overview.enrollment_start = datetime.utcnow() - timedelta(days=180)
        re_run_course_overview.enrollment_end = datetime.utcnow() - timedelta(days=152)

        re_run_course_overview.save()

        rerun_parent_course_overview = CourseOverview.get_from_id(course_id=self.rerun_parent_course.id)

        rerun_parent_course_overview.end = datetime.utcnow() - timedelta(days=60)
        rerun_parent_course_overview.start = datetime.utcnow() - timedelta(days=75)
        rerun_parent_course_overview.enrollment_start = datetime.utcnow() - timedelta(days=90)
        rerun_parent_course_overview.enrollment_end = datetime.utcnow() - timedelta(days=76)

        rerun_parent_course_overview.save()

        self.assertIsNone(get_future_courses(self.rerun_parent_course.id))

        re_run_course_overview.end = datetime.utcnow() + timedelta(days=30)
        re_run_course_overview.start = datetime.utcnow() + timedelta(days=16)
        re_run_course_overview.enrollment_start = datetime.utcnow() + timedelta(days=5)
        re_run_course_overview.enrollment_end = datetime.utcnow() + timedelta(days=15)

        re_run_course_overview.save()

        rerun_parent_course_overview.end = datetime.utcnow() - timedelta(days=60)
        rerun_parent_course_overview.start = datetime.utcnow() - timedelta(days=75)
        rerun_parent_course_overview.enrollment_start = datetime.utcnow() - timedelta(days=90)
        rerun_parent_course_overview.enrollment_end = datetime.utcnow() - timedelta(days=76)

        rerun_parent_course_overview.save()

        self.assertEqual(get_future_courses(self.rerun_parent_course.id), re_run_course_overview)

        re_run_course_overview.end = datetime.utcnow() + timedelta(days=300)
        re_run_course_overview.start = datetime.utcnow() + timedelta(days=160)
        re_run_course_overview.enrollment_start = datetime.utcnow() + timedelta(days=50)
        re_run_course_overview.enrollment_end = datetime.utcnow() + timedelta(days=150)

        re_run_course_overview.save()

        rerun_parent_course_overview.end = datetime.utcnow() + timedelta(days=30)
        rerun_parent_course_overview.start = datetime.utcnow() + timedelta(days=16)
        rerun_parent_course_overview.enrollment_start = datetime.utcnow() + timedelta(days=5)
        rerun_parent_course_overview.enrollment_end = datetime.utcnow() + timedelta(days=15)

        rerun_parent_course_overview.save()

        self.assertEqual(get_future_courses(self.rerun_parent_course.id), re_run_course_overview)

    def test_is_course_rereun(self):
        non_re_run_course_id = self.courses[1].id
        parent_course_id = self.rerun_parent_course.id
        re_run_course_id = self.re_run_course.id

        # Desired output is the parent's course id
        self.assertEqual(is_course_rereun(re_run_course_id), parent_course_id)

        # For courses without a rerun the None is returned
        self.assertIsNone(is_course_rereun(non_re_run_course_id))

        # For parent course id as input, None should be returned
        self.assertIsNone(is_course_rereun(parent_course_id))

    def test_get_course_cards_list(self):
        # Disable a course's course card
        course = self.courses[-1]
        course_card = CourseCard.objects.get(course_id=course.id)
        course_card.is_enabled = False
        course_card.save()

        request = RequestFactory().get('/dummy-url')
        request.user = self.user
        request.session = {}
        set_current_request(request)

        # For Normal User
        # Desired output is a list of course overview objects for which course card is enabled
        self.assertEqual({c.id for c in get_course_cards_list()}, {course.id for course in self.courses[:-1]})

        request.user = self.staff
        set_current_request(request)

        # For Staff User
        # Desired output is a list of all course overview objects
        self.assertEqual({c.id for c in get_course_cards_list()}, {course.id for course in self.courses})

    def test_initialize_course_settings(self):
        parent_course_id = self.rerun_parent_course.id
        re_run_course_id = self.re_run_course.id

        custom_tags = '{"test_key": "test_value"}'
        custom_settings = CustomSettings.objects.get(id=parent_course_id)

        custom_settings.tags = custom_tags
        custom_settings.save()

        initialize_course_settings(parent_course_id, re_run_course_id)

        # Desired output is that the tags have been set in the rerun course custom settings as per the parent course
        self.assertEqual(CustomSettings.objects.get(id=re_run_course_id).tags, custom_tags)

        # If parent course id is not provided or is none method returns none
        self.assertIsNone(initialize_course_settings(None, re_run_course_id))
