from django.http import Http404

from xmodule.modulestore import ModuleStoreEnum
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory

from openedx.features.partners import helpers
from openedx.core.djangoapps.models.course_details import CourseDetails


class PartnerHelpersTest(ModuleStoreTestCase):
    """ Test cases for helpers """

    PARTNER_SLUG = "give2asia"
    ATTRIBUTE_NAME = "description"

    def setUp(self):
        super(PartnerHelpersTest, self).setUp()
        self.course = CourseFactory.create()

    def test_import_module_using_slug_with_valid_slug(self):
        views = helpers.import_module_using_slug(self.PARTNER_SLUG)
        self.assertNotEqual(views, None)

    def test_import_module_using_slug_with_invalid_slug(self):
        with self.assertRaises(Http404) as e:
            helpers.import_module_using_slug('invalid')
        self.assertEqual(e.exception.message, 'Your partner is not properly registered')

    def test_get_course_description(self):
        attribute_value = 'description value'
        with self.store.branch_setting(ModuleStoreEnum.Branch.draft_preferred, self.course.id):
            CourseDetails.update_about_item(self.course, self.ATTRIBUTE_NAME, attribute_value, self.user.id)
        self.assertEqual(CourseDetails.fetch_about_attribute(self.course.id, self.ATTRIBUTE_NAME), attribute_value)

    def test_get_course_description_with_invalid_description(self):
        attribute_value = 'description value'
        with self.store.branch_setting(ModuleStoreEnum.Branch.draft_preferred, self.course.id):
            CourseDetails.update_about_item(self.course, self.ATTRIBUTE_NAME, attribute_value, self.user.id)
        self.assertNotEqual(CourseDetails.fetch_about_attribute(self.course.id, self.ATTRIBUTE_NAME), 'invalid description value')


