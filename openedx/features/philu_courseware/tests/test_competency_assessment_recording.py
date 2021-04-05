"""
All tests for competency assessment recording
"""
from copy import deepcopy

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from openedx.features.philu_courseware.constants import INVALID_PROBLEM_ID_MSG
from student.tests.factories import UserFactory

INVALID_ASSESSMENT_TYPE = 'This is invalid assessment type'
INVALID_CORRECTNESS = 'This is invalid correctness'
NOT_VALID_CHOICE_FORMAT = '"{}" is not a valid choice.'


class CompetencyAssessmentRecordTest(APITestCase):
    """
    All tests for saving user attempts and get assessment scores
    """

    def setUp(self):
        super(CompetencyAssessmentRecordTest, self).setUp()
        self.user = UserFactory()
        self.client.force_authenticate(self.user)  # pylint: disable=no-member
        self.end_point = reverse('competency_assessment', kwargs=dict(chapter_id=1))
        self.valid_record = {
            'chapter_id': 'test-chapter',
            'problem_id': 'block-v1:PUCIT+IT1+1+type@problem+block@7f1593ef300e4f569e26356b65d3b76b',
            'problem_text': 'This is a problem',
            'assessment_type': 'pre',
            'attempt': 1,
            'correctness': 'correct',
            'choice_id': 1,
            'choice_text': 'This is correct choice',
            'score': 1
        }

    def test_valid_record(self):
        """
        Test valid records, and assert response is 201
        """
        response = self.client.post(
            self.end_point,
            data=[self.valid_record], format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_problem_id(self):
        """
        Test invalid records, and assert response is 400
        """
        record = deepcopy(self.valid_record)
        record['problem_id'] = 'this_is_invalid_problem_id'

        response = self.client.post(
            self.end_point,
            data=[record], format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(INVALID_PROBLEM_ID_MSG, response.data[0]['problem_id'])

    def test_invalid_correctness_and_assessment_type(self):
        """
        Test invalid correctness and assessment type, and assert response is 400
        """
        record = deepcopy(self.valid_record)
        record['assessment_type'] = INVALID_ASSESSMENT_TYPE
        record['correctness'] = INVALID_CORRECTNESS

        response = self.client.post(
            self.end_point,
            data=[record], format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(NOT_VALID_CHOICE_FORMAT.format(INVALID_ASSESSMENT_TYPE), response.data[0]['assessment_type'])
        self.assertIn(NOT_VALID_CHOICE_FORMAT.format(INVALID_CORRECTNESS), response.data[0]['correctness'])

    def test_all_missing_keys(self):
        """
        Test all missing keys, and assert response is 400
        """
        for key in self.valid_record:
            record = deepcopy(self.valid_record)
            record.pop(key)  # pop the key we want to miss
            self._assert_missing_keys(record, key)

    def _assert_missing_keys(self, pay_load, missing_key):
        """
        A collection of assert statements for competency assessment recording response
        """
        response = self.client.post(
            self.end_point,
            data=[pay_load], format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(missing_key, response.data[0].keys())
        self.assertIn('This field is required.', response.data[0][missing_key])
