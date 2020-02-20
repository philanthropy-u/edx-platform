from organizations.tests.factories import UserFactory

from openedx.core.djangoapps.models.course_details import CourseDetails
from openedx.features.partners import helpers
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory


class PartnerHelpersTest(ModuleStoreTestCase):
    """ Test cases for openedx partner feature helpers """

    ATTRIBUTE_NAME = 'description'

    def setUp(self):
        super(PartnerHelpersTest, self).setUp()
        self.user = UserFactory()
        self.course = CourseFactory.create()

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
