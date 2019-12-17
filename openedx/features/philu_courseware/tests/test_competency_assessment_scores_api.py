"""Unit tests for pre post assessment scores api"""

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from openedx.features.philu_courseware import constants
from student.tests.factories import UserFactory, CourseEnrollmentFactory
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory, ItemFactory


class PrePostAssessmentMixin(ModuleStoreTestCase):
    """Mixin for pre/post assessments score tests"""

    def create_course_and_user(self):
        """
        Create user and a simple course for testing pre/post assessments score api.
        """
        self.course = CourseFactory.create(display_name='test_course', number='100')
        self.user = UserFactory.create(username='dummy', password='foo')
        self.add_competency_assessment_grading_policy()

    def create_chapter(self):
        """Create chapter in course"""
        return ItemFactory.create(
            parent_location=self.course.location,
            category='chapter',
            display_name='Chapter'
        )

    def create_assessment_subsection(self, chapter, assessment_format=constants.PRE_ASSESSMENT_FORMAT):
        """Create pre/post assessment in module/chapter"""
        return ItemFactory.create(
            parent_location=chapter.location,
            display_name=assessment_format,
            category='sequential',
            metadata={'graded': True, 'format': assessment_format}
        )

    def get_competency_assessment_api_response(self, chapter_id):
        """Method to create url and call api"""
        url = reverse(
            'competency_assessments_score',
            kwargs={
                'course_id': self.course.id,
                'chapter_id': chapter_id,
            }
        )

        return self.client.get(url)

    def add_competency_assessment_grading_policy(self):
        """Add grading policy to mark assessments pre or post for testing"""
        grading_policy = {
            "GRADER": [
                {
                    "type": constants.PRE_ASSESSMENT_FORMAT,
                    "min_count": 1,
                    "drop_count": 0,
                    "short_label": constants.PRE_ASSESSMENT_FORMAT,
                    "weight": 0.0
                },
                {
                    "type": constants.POST_ASSESSMENT_FORMAT,
                    "min_count": 1,
                    "drop_count": 0,
                    "short_label": constants.POST_ASSESSMENT_FORMAT,
                    "weight": 0.25
                }
            ]
        }

        self.course.grading_policy = grading_policy
        self.update_course(self.course, self.user.id)
        self.course = self.store.get_course(self.course.id)


class PrePostAssessmentScoreForUnEnrolledUserTest(PrePostAssessmentMixin, APITestCase):
    """Tests for unenrolled and unauthorized users"""

    def setUp(self):
        super(PrePostAssessmentScoreForUnEnrolledUserTest, self).setUp()
        self.create_course_and_user()
        self.client.force_authenticate(self.user)

    def test_un_enrolled_user_request(self):
        """Test unenrolled user request"""
        response = self.get_competency_assessment_api_response(self.create_chapter().location.block_id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_request(self):
        """Test unauthorized request"""
        self.client.force_authenticate(user=None)
        response = self.get_competency_assessment_api_response(self.create_chapter().location.block_id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrePostAssessmentScoreForEnrolledUserTest(PrePostAssessmentMixin, APITestCase):
    """Tests for enrolled users"""

    def setUp(self):
        super(PrePostAssessmentScoreForEnrolledUserTest, self).setUp()
        self.create_course_and_user()
        self.client.force_authenticate(self.user)
        CourseEnrollmentFactory.create(user=self.user, course_id=self.course.id)

    def test_invalid_chapter_id(self):
        """Test api for invalid chapter id"""
        response = self.get_competency_assessment_api_response('invalid_chapter_id')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_no_competency_assessment_in_chapter(self):
        """Test if module/chapter has no pre/post assessment"""
        chapter = self.create_chapter()
        ItemFactory.create(
            parent_location=chapter.location,
            display_name='Welcome',
            category='sequential'
        )
        response = self.get_competency_assessment_api_response(chapter.location.block_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_only_pre_assessment_chapter(self):
        """Test module/chapter has only pre assessment"""
        chapter = self.create_chapter()
        self.create_assessment_subsection(chapter)
        response = self.get_competency_assessment_api_response(chapter.location.block_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_only_post_assessment_chapter(self):
        """Test module/chapter has only post assessment"""
        chapter = self.create_chapter()
        self.create_assessment_subsection(chapter, constants.POST_ASSESSMENT_FORMAT)
        response = self.get_competency_assessment_api_response(chapter.location.block_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_competency_assessment_chapter(self):
        """Test module/chapter has both pre and post assessments"""
        chapter = self.create_chapter()
        self.create_assessment_subsection(chapter)
        self.create_assessment_subsection(chapter, constants.POST_ASSESSMENT_FORMAT)
        response = self.get_competency_assessment_api_response(chapter.location.block_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['all_pre_assessment_attempted'])
        self.assertFalse(response.data['all_post_assessment_attempted'])
        self.assertFalse(response.data['pre_assessment_attempted'])
        self.assertEqual(response.data['pre_assessment_score'], 0.0)
        self.assertEqual(response.data['post_assessment_score'], 0.0)
