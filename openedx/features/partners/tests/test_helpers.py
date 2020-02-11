from datetime import datetime, timedelta
from django.contrib.auth.models import Permission
from django.http import Http404
from mock import patch

from organizations.tests.factories import UserFactory
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory

from openedx.core.djangoapps.models.course_details import CourseDetails
from openedx.features.partners import helpers
from openedx.features.partners.tests.factories import (CourseCardFactory, CourseOverviewFactory, CustomSettingsFactory,
                                                       PartnerCommunityFactory, PartnerFactory, PartnerUserFactory)


class PartnerHelpersTest(ModuleStoreTestCase):
    """ Test cases for openedx partner feature helpers """

    PARTNER_SLUG = "give2asia"
    ATTRIBUTE_NAME = "description"
    PARTNER_PERMISSION = "can_access_{slug}_performance".format(slug=PARTNER_SLUG)
    ORGANIZATION = "arbisoft"

    def setUp(self):
        super(PartnerHelpersTest, self).setUp()
        self.user = UserFactory()
        self.partner = PartnerFactory.create(slug=self.PARTNER_SLUG, label=self.ORGANIZATION)
        self.partner_user = PartnerUserFactory(user=self.user, partner=self.partner)
        self.course = CourseFactory.create()

    def test_import_module_using_slug_with_valid_slug(self):
        """
        Test if view is available for a valid slug
        :return : partner view
        """
        views = helpers.import_module_using_slug(self.PARTNER_SLUG)
        self.assertNotEqual(views, None)

    def test_import_module_using_slug_with_invalid_slug(self):
        """
        Test 404 is returned for an invalid partner slug
        :return : None
        """
        with self.assertRaises(Http404) as error:
            helpers.import_module_using_slug('invalid')
        self.assertEqual(error.exception.message, 'Your partner is not properly registered')

    def test_get_course_description(self):
        """
        Create a course and update its description
        Verify that valid description is returned from helper function
        :return : course description
        """
        attribute_value = 'description value'
        CourseDetails.update_about_item(self.course, self.ATTRIBUTE_NAME, attribute_value, self.user.id)

        self.assertEqual(
            CourseDetails.fetch_about_attribute(self.course.id, self.ATTRIBUTE_NAME),
            helpers.get_course_description(self.course)
        )

    def test_get_course_description_with_invalid_course(self):
        """
        Verify that empty string is returned for invalid course
        """
        self.assertEqual(helpers.get_course_description(None), '')

    def test_get_partner_recommended_courses_with_valid_partner(self):
        """
        Create Custom settings, Course overview and Course Card
        :return : list of recommended courses
        """
        CustomSettingsFactory(id=self.course.id, tags=self.PARTNER_SLUG)
        CourseOverviewFactory(id=self.course.id)
        CourseCardFactory(course_id=self.course.id, course_name=self.course.name)

        recommended_courses = helpers.get_partner_recommended_courses(self.PARTNER_SLUG, self.user)

        self.assertNotEqual(len(recommended_courses), 0)

    def test_get_partner_recommended_courses_with_invalid_custom_settings(self):
        """
        Create Custom settings with invalid partner slug
        Create Course overview and and Course Card
        :return : list of recommended courses
        """
        CustomSettingsFactory(id=self.course.id, tags="invalid")
        CourseOverviewFactory(id=self.course.id)
        CourseCardFactory(course_id=self.course.id, course_name=self.course.name)

        recommended_courses = helpers.get_partner_recommended_courses(self.PARTNER_SLUG, self.user)

        self.assertEqual(len(recommended_courses), 0)

    def test_get_partner_recommended_courses_without_course_card(self):
        """
        Create Custom settings for partner
        Create Course overview
        :return : list of recommended courses
        """
        CustomSettingsFactory(id=self.course.id, tags=self.PARTNER_SLUG)
        CourseOverviewFactory(id=self.course.id)

        recommended_courses = helpers.get_partner_recommended_courses(self.PARTNER_SLUG, self.user)

        self.assertEqual(len(recommended_courses), 0)

    def test_get_partner_recommended_courses_with_invalid_partner(self):
        """
        Test empty list of recommendation is returned for invalid partner
        :return : list of recommended courses
        """
        recommended_courses = helpers.get_partner_recommended_courses("invalid", self.user)
        self.assertEqual(len(recommended_courses), 0)

    def test_get_partner_recommended_courses_with_invalid_enrollment_start_date(self):
        """
        Test empty list of recommendation is returned if enrolment start date is in the future
        :return : list of recommended courses
        """
        # get a future date
        enrollment_date = datetime.now() + timedelta(days=2)
        CourseOverviewFactory(id=self.course.id, enrollment_start=enrollment_date)

        recommended_courses = helpers.get_partner_recommended_courses(self.PARTNER_SLUG, self.user)
        self.assertEqual(len(recommended_courses), 0)

    def test_get_partner_recommended_courses_with_invalid_enrollment_end_date(self):
        """
        Test empty list of recommendation is returned if enrolment end is in the past
        :return : list of recommended courses
        """
        # get a future date
        enrollment_date = datetime.now() + timedelta(days=-2)
        CourseOverviewFactory(id=self.course.id, enrollment_start=enrollment_date)

        recommended_courses = helpers.get_partner_recommended_courses(self.PARTNER_SLUG, self.user)
        self.assertEqual(len(recommended_courses), 0)

    @patch('openedx.features.partners.helpers.log.info')
    def test_auto_join_partner_community_with_valid_partner_community(self, mock_log_info):
        """
        log.info method gets called when task is successfully
        added to celery. Using mock make sure that log.info gets
        called
        Create a partner and partner community
         :return : None
        """
        PartnerCommunityFactory(partner=self.partner)
        helpers.auto_join_partner_community(self.partner, self.user)
        assert mock_log_info.called_once

    @patch('openedx.features.partners.helpers.log.info')
    def test_auto_join_partner_community_with_multiple_partner_community(self, mock_log_info):
        """
        Test that log.info method gets called for all added
        communities for a partner
        Create 2 partner communities
        :return : None
        """
        PartnerCommunityFactory(partner=self.partner)
        PartnerCommunityFactory(partner=self.partner)
        helpers.auto_join_partner_community(self.partner, self.user)
        self.assertEqual(mock_log_info.call_count, 2)

    @patch('openedx.features.partners.helpers.log.info')
    def test_auto_join_partner_community_without_partner_community(self, mock_log_info):
        """
        log.info method gets called when task is successfully
        added to celery. Using mock make sure that log.info gets
        called
        :return : None
        """
        helpers.auto_join_partner_community(self.partner, self.user)
        assert mock_log_info.not_called

    def test_get_partner_from_user_with_partner(self):
        """
        Test that valid partner object is returned against user
        :return: partner
        """
        self.assertEqual(helpers.get_partner_from_user(self.user), self.partner)

    def test_get_partner_from_user_without_partner_user_relation(self):
        """
        Test that none is returned if a bridget between user and partner
        is not created
        @return: partner
        """
        user = UserFactory()
        self.assertEqual(helpers.get_partner_from_user(user), None)

    def test_user_has_performance_access_with_permission(self):
        """
        Test that a valid user has access to
        Give user permission to access performance page
        :return: bool
        """
        permission = Permission.objects.filter(codename=self.PARTNER_PERMISSION).first()
        if permission:
            self.user.user_permissions.add(permission)
        self.assertEqual(helpers.user_has_performance_access(self.user, self.partner), True)

    def test_user_has_performance_access__without_permission(self):
        """
        Test user is unable to access performance page without a valid permission
        Create a new user
        :return: bool
        """
        user = UserFactory()
        self.assertEqual(helpers.user_has_performance_access(user, self.partner), False)
