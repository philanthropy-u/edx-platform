from django.contrib.auth.models import User
from django.test import TestCase

from ..views import get_course_cards
from ..models import CourseCard
from django.core.urlresolvers import reverse

from xmodule.modulestore.django import modulestore
from xmodule.modulestore.tests.factories import CourseFactory
from xmodule.modulestore import ModuleStoreEnum
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase

from datetime import datetime, timedelta
from pyquery import PyQuery as pq

from openedx.core.djangoapps.theming.models import SiteTheme
from django.contrib.sites.models import Site

from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from student.tests.factories import UserFactory, CourseEnrollmentFactory

from student.models import UserProfile
from lms.djangoapps.onboarding.models import UserExtendedProfile, EmailPreference, Organization
from common.lib.nodebb_client.client import NodeBBClient


class CourseCardBaseClass(ModuleStoreTestCase):

    password = 'test'
    # Always keep greater than equal to 2
    NUMBER_OF_COURSES = 4

    def setUp(self):
        super(CourseCardBaseClass, self).setUp()

        self.user = UserFactory(password=self.password)
        self.staff = UserFactory(is_staff=True, password=self.password)

        for user in [self.user, self.staff]:
            email_preference = EmailPreference(
                user=user,
                opt_in="no",

            )
            email_preference.save()

            user_profile = UserProfile.objects.get(user=user)
            user_profile.name = "{} {}".format(user.first_name, user.last_name)
            user_profile.level_of_education = 'b'

            user_profile.save()

            extended_profile = UserExtendedProfile(
                user=user,
                is_interests_data_submitted=True,
                english_proficiency="Master",
            )
            extended_profile.save()

            organization = Organization(
                admin=user,
                alternate_admin_email=user.email,
            )
            organization.save()
            organization.unclaimed_org_admin_email = user.email
            organization.alternate_admin_email = None
            organization.save()

        org = 'edX'
        course_number_f = 'CS10{}'
        course_run = '2015_Q1'
        display_name_f = 'test course {}'

        self.courses = [
            CourseFactory.create(org=org, number=course_number_f.format(str(i)), run=course_run,
                                 display_name=display_name_f.format(str(i)), default_store=ModuleStoreEnum.Type.split)
            for i in range(1, self.NUMBER_OF_COURSES + 1)
        ]

        for course in self.courses:
            course.save()
            CourseCard(course_id=course.id, course_name=course.display_name, is_enabled=True).save()




        # CourseOverview.get_from_id(self.course.id)
        # CourseEnrollmentFactory.create(user=student, course_id=self.course.id)

    @classmethod
    def setUpClass(cls):
        super(CourseCardBaseClass, cls).setUpClass()
        site = Site(domain='testserver', name='test')
        site.save()
        theme = SiteTheme(site=site, theme_dir_name='philu')
        theme.save()

    def test_enabled_courses_view(self):
        course = self.courses[0]
        course_card = CourseCard.objects.get(course_id=course.id)
        course_card.is_enabled = False

        course_card.save()

        self.client.login(username=self.staff.username, password=self.password)
        response = self.client.get(reverse('courses'))

        # desired output is NUMBER_OF_COURSES since despite one course's course card being disabled,
        # Staff user is still able to see it in the course list
        self.assertEqual(pq(response.content)("article.course").length, len(self.courses))

        self.client.logout()

        self.client.login(username=self.user.username, password=self.password)
        response = self.client.get(reverse('courses'))

        # desired output is (NUMBER_OF_COURSES - 1) since one course's course card has been disabled,
        # and normal user should not be able to see disabled courses
        self.assertEqual(pq(response.content)("article.course").length, len(self.courses)-1)

    def test_no_scheduled_or_ended_classes_case(self):
        ended_course = self.courses[0]
        scheduled_courses = self.courses[2:]

        ended_course_overview = CourseOverview.get_from_id(course_id=ended_course.id)

        ended_course_overview.end = datetime.utcnow() - timedelta(days=60)
        ended_course_overview.start = datetime.utcnow() - timedelta(days=75)
        ended_course_overview.enrollment_start = datetime.utcnow() - timedelta(days=90)
        ended_course_overview.enrollment_end = datetime.utcnow() - timedelta(days=76)

        ended_course_overview.save()

        for scheduled_course in scheduled_courses:
            scheduled_course_overview = CourseOverview.get_from_id(course_id=scheduled_course.id)

            scheduled_course_overview.end = datetime.utcnow() + timedelta(days=75)
            scheduled_course_overview.start = datetime.utcnow() + timedelta(days=60)
            scheduled_course_overview.enrollment_start = datetime.utcnow() + timedelta(days=30)
            scheduled_course_overview.enrollment_end = datetime.utcnow() + timedelta(days=59)

            scheduled_course_overview.save()

        response = self.client.get(reverse('courses'))

        # Desired output is 2 since there is one course that has not been assigned
        # any start or end date and another course that has already ended
        self.assertEqual(pq(response.content)("span.no-scheduled-class").length, 2)

    def test_ongoing_course_start_date(self):
        ongoing_course = self.courses[0]

        ongoing_course_overview = CourseOverview.get_from_id(course_id=ongoing_course.id)

        ongoing_course_overview.end = datetime.utcnow() + timedelta(days=30)
        ongoing_course_overview.start = datetime.utcnow() + timedelta(days=16)
        ongoing_course_overview.enrollment_start = datetime.utcnow() - timedelta(days=15)
        ongoing_course_overview.enrollment_end = datetime.utcnow() + timedelta(days=5)

        ongoing_course_overview.save()

        response = self.client.get(reverse('courses'))

        # Desired Result is one since only one ongoing course
        self.assertEqual(pq(response.content)('span.text:contains("Start Date")').length, 1)

    def test_start_date_value(self):
