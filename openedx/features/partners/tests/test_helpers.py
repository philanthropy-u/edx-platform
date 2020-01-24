from django.http import Http404
from organizations.tests.factories import UserFactory

from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory

from openedx.features.partners import helpers
from openedx.core.djangoapps.models.course_details import CourseDetails
from openedx.features.partners.tests.factories import CustomSettingsFactory, CourseCardFactory, CourseOverviewFactory, \
    PartnerFactory


class PartnerHelpersTest(ModuleStoreTestCase):
    """ Test cases for openedx partner feature helpers """

    PARTNER_SLUG = "give2asia"
    ATTRIBUTE_NAME = "description"

    def setUp(self):
        super(PartnerHelpersTest, self).setUp()
        self.user = UserFactory()
        self.partner = PartnerFactory.create(slug=self.PARTNER_SLUG, label='arbisoft')
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
        with self.assertRaises(Http404) as e:
            helpers.import_module_using_slug('invalid')
        self.assertEqual(e.exception.message, 'Your partner is not properly registered')

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
        Create Custom settings , Course overview and Course Card
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
        Test empty list of recommendation is returned for in valid partner
        :return : list of recommended courses
        """
        recommended_courses = helpers.get_partner_recommended_courses("invalid", self.user)
        self.assertEqual(len(recommended_courses), 0)

