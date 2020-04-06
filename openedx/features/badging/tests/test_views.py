import ddt as ddt
import mock
import json
from mock import call

from django.core.urlresolvers import reverse
from django.http import Http404
from django.test import RequestFactory
from django.test.client import Client

from openedx.core.djangoapps.xmodule_django.models import CourseKeyField
from student.tests.factories import CourseEnrollmentFactory
from student.tests.factories import UserFactory
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory

from nodebb.constants import CONVERSATIONALIST_ENTRY_INDEX, TEAM_PLAYER_ENTRY_INDEX

from .factories import BadgeFactory, UserBadgeFactory, DiscussionCommunityFactory
from .. import views as badging_views
from ..constants import (
    COURSES_KEY,
    CONVERSATIONALIST,
    DISCUSSION_ID_KEY,
    DISCUSSION_COUNT_KEY,
    USERNAME_KEY
)

STATUS_CODE_TRUE = 200
STATUS_CODE_FALSE = 400


@ddt.ddt
class BadgeViewsTestCases(ModuleStoreTestCase):

    def setUp(self):
        super(BadgeViewsTestCases, self).setUp()
        self.course = CourseFactory(org="test", number="123", run="1")
        self.request_factory = RequestFactory()
        self.user = UserFactory()

    def test_trophycase_with_various_course(self):
        """
        Create 2 courses and their course enrollments (1 active & 1 inactive), without badges.
        Assert that response code is 200 and expected json has data for only active course enrollment
        :return: None
        """
        request = self.request_factory.get(reverse('trophycase'), {'json': True})
        request.user = self.user

        # create two courses here, one is already created via setUp
        course1 = CourseFactory(org="test1", number="123", run="1", display_name="course1")
        course2 = CourseFactory(org="test2", number="123", run="1", display_name="course2")

        # enroll in two course one of which is active other is inactive
        CourseEnrollmentFactory(user=self.user, course_id=course1.id, is_active=True)
        CourseEnrollmentFactory(user=self.user, course_id=course2.id, is_active=False)

        response = badging_views.trophycase(request)

        expected_json = """{"test1/123/1":{"display_name":"course1","badges":{"conversationalist":[]}}}"""
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_json)

    @mock.patch('openedx.features.badging.views.populate_trophycase')
    def test_trophycase_with_some_earned_badges(self, mock_populate_trophycase):
        """
        Test trophy case for 2 badges, one badge earned by current user and both badges earned by some other user.
        Assert that request is fetching data for only current logged in user for the badges only he has earned
        in relevant course. And Badge earned by other user are ignored
        :param mock_populate_trophycase: mock to assert it has been called with expected input
        :return: None
        """
        request = self.request_factory.get(reverse('trophycase'), {'json': True})
        request.user = self.user

        badge1 = BadgeFactory()
        badge2 = BadgeFactory()

        # Assign one badge to current user
        user_badge = UserBadgeFactory(user=self.user, badge=badge1)
        # Assign few badge to any other users
        any_other_user = UserFactory()
        UserBadgeFactory(user=any_other_user, course_id=user_badge.course_id, badge=badge1)
        UserBadgeFactory(user=any_other_user, course_id=CourseKeyField.Empty, badge=badge2)

        mock_populate_trophycase.return_value = dict()
        badging_views.trophycase(request)
        mock_populate_trophycase.assert_called_once_with(request.user, mock.ANY, [user_badge])

    @ddt.data(STATUS_CODE_TRUE, STATUS_CODE_FALSE)
    @mock.patch('openedx.features.badging.views.render_to_response')
    @mock.patch('openedx.features.badging.views.add_posts_count_in_badges_list')
    @mock.patch('openedx.features.badging.views.NodeBBClient')
    @mock.patch('openedx.features.badging.views.get_badge_progress_request_data')
    @mock.patch('openedx.features.badging.views.get_discussion_team_ids')
    def test_trophycase_get_progress_api(self, api_status_code, mock_get_discussion_team_ids,
                                         mock_get_badge_progress_request_data,
                                         mock_nodebb_client,
                                         mock_add_posts_count_in_badges_list,
                                         mock_render_response):
        """
        Test nodeBB api client call arguments and its response. Api will node be called it is mocked so we are just
        setting response of api and later check if that response is using or not.
        :param api_status_code: Status code that will be used to test both positive and negative case
        :param mock_get_discussion_team_ids: mock get_discussion_team_ids helper method
        :param mock_get_badge_progress_request_data: mock get_badge_progress_request_data helper method
        :param mock_nodebb_client: mock NodeBB Client class
        :param mock_add_posts_count_in_badges_list: mock add_posts_count_in_badges_list helper method
        :param mock_render_response: mock render_to_response method because we are having problems with our templates
        :return: None
        """
        request = self.request_factory.get(reverse('trophycase'), {'json': True})
        request.user = self.user

        second_course = CourseFactory(org="test", number="456", run="1")

        # Enroll user in both courses
        CourseEnrollmentFactory(user=self.user, course_id=self.course.id, is_active=True)
        CourseEnrollmentFactory(user=self.user, course_id=second_course.id, is_active=True)

        DiscussionCommunityFactory(course_id=self.course.id, community_url='100/abc')
        DiscussionCommunityFactory(course_id=second_course.id, community_url='101/abc')

        courses_discussion_data = [
            {str(self.course.id): {DISCUSSION_ID_KEY: 100}},
            {str(second_course.id): {DISCUSSION_ID_KEY: 101}}
        ]

        badges, sample_api_request, sample_api_response = get_all_data_dicts(self, courses_discussion_data)

        courses_discussion_data[0][str(self.course.id)][DISCUSSION_COUNT_KEY] = 3  # Could be any number
        courses_discussion_data[1][str(second_course.id)][DISCUSSION_COUNT_KEY] = 2  # Could be any number

        mock_get_discussion_team_ids.return_value = courses_discussion_data
        mock_get_badge_progress_request_data.return_value = sample_api_request
        mock_nodebb_client.return_value.badges.get_progress = mock.MagicMock(
            return_value=(api_status_code, sample_api_response))

        badging_views.trophycase(request)

        mock_nodebb_client.return_value.badges.get_progress.assert_called_once_with(request_data=sample_api_request)

        if api_status_code == STATUS_CODE_TRUE:
            mock_add_posts_count_in_badges_list.assert_has_calls([call(sample_api_response[COURSES_KEY][0], badges),
                                                                  call(sample_api_response[COURSES_KEY][1], badges)])
            self.assertEqual(mock_add_posts_count_in_badges_list.call_count, 2)
        else:
            self.assertEqual(mock_add_posts_count_in_badges_list.call_count, 0)

    def test_my_badges_denies_anonymous(self):
        """
        This method test API call without logged-in user. In this case user must be redirected
        to login page
        :return: None
        """
        path = reverse('my_badges', kwargs={'course_id': 'course/123/1'})
        response = Client().get(path=path)
        self.assertRedirects(response, '{}?next={}'.format(reverse('signin_user'), path))

    def test_my_badges_invalid_course_id(self):
        """
        Test my badges with invalid course id. Assert that an error is raised
        :return: None
        """
        course_id = 'test/course/123'
        path = reverse('my_badges', kwargs={'course_id': course_id})

        request = self.request_factory.get(path)
        request.user = self.user

        with self.assertRaises(Http404):
            badging_views.my_badges(request, course_id)

    @mock.patch('openedx.features.badging.views.render_to_response')
    @mock.patch('openedx.features.badging.views.get_badge_progress_request_data')
    @mock.patch('openedx.features.badging.views.get_discussion_team_ids')
    @mock.patch('openedx.features.badging.views.get_course_badges')
    def test_my_badges_with_enrolled_and_active_course(self, mock_get_course_badges, mock_get_discussion_team_ids,
                                                       mock_get_badge_progress_request_data, mock_response):
        """
        Test my badges with 1 active course enrollment for valid course
        :param mock_get_course_badges: mock to assert it has been called with expected input
        :return: None
        """
        CourseEnrollmentFactory(user=self.user, course_id=self.course.id, is_active=True)

        path = reverse('my_badges', kwargs={'course_id': self.course.id})
        request = self.request_factory.get(path)
        request.user = self.user

        mock_get_course_badges.return_value = dict()
        mock_get_discussion_team_ids.return_value = dict()
        mock_get_badge_progress_request_data.return_value = {}
        mock_response.return_value = mock.ANY

        badging_views.my_badges(request, self.course.id)
        mock_get_course_badges.assert_called_once_with(request.user, self.course.id, list())

    def test_my_badges_with_enrolled_but_inactive_course(self):
        """
        Test my badges with inactive course. Assert that an error is raised
        :return: None
        """
        CourseEnrollmentFactory(user=self.user, course_id=self.course.id, is_active=False)

        path = reverse('my_badges', kwargs={'course_id': self.course.id})
        request = self.request_factory.get(path)
        request.user = self.user

        with self.assertRaises(Http404):
            badging_views.my_badges(request, self.course.id)

    @mock.patch('openedx.features.badging.views.get_course_badges')
    def test_my_badges_with_some_earned_badges(self, mock_get_course_badges):
        """
        Test my badges for 2 badges, one badge earned by current user and both badges earned by some other user.
        Assert that request is fetching data for only current logged in user for the badges only he has earned
        in relevant course. And Badge earned by other user are ignored
        :param mock_get_course_badges: mock to assert it has been called with expected input
        :return: None
        """
        CourseEnrollmentFactory(user=self.user, course_id=self.course.id, is_active=True)

        path = reverse('my_badges', kwargs={'course_id': self.course.id})
        request = self.request_factory.get(path)
        request.user = self.user

        badge1 = BadgeFactory()
        badge2 = BadgeFactory()

        # Assign one badge to current user
        user_badge = UserBadgeFactory(user=self.user, course_id=self.course.id, badge=badge1)
        # Assign few badge to any other users
        any_other_user = UserFactory()
        UserBadgeFactory(user=any_other_user, course_id=self.course.id, badge=badge1)
        UserBadgeFactory(user=any_other_user, course_id=self.course.id, badge=badge2)

        mock_get_course_badges.return_value = dict()
        badging_views.my_badges(request, self.course.id)
        mock_get_course_badges.assert_called_once_with(request.user, self.course.id, [user_badge])

    @ddt.data(STATUS_CODE_TRUE, STATUS_CODE_FALSE)
    @mock.patch('openedx.features.badging.views.render_to_response')
    @mock.patch('openedx.features.badging.views.add_posts_count_in_badges_list')
    @mock.patch('openedx.features.badging.views.NodeBBClient')
    @mock.patch('openedx.features.badging.views.get_badge_progress_request_data')
    @mock.patch('openedx.features.badging.views.get_discussion_team_ids')
    def test_my_badges_get_progress_api(self, api_status_code, mock_get_discussion_team_ids,
                                        mock_get_badge_progress_request_data,
                                        mock_nodebb_client,
                                        mock_add_posts_count_in_badges_list,
                                        mock_render_response):
        """
        Test nodeBB api client call arguments and its response. Api will node be called it is mocked so we are just
        setting response of api and later check if that response is using or not.
        :param api_status_code: Status code that will be used to test both positive and negative case
        :param mock_get_discussion_team_ids: mock get_discussion_team_ids helper method
        :param mock_get_badge_progress_request_data: mock get_badge_progress_request_data helper method
        :param mock_nodebb_client: mock NodeBB Client class
        :param mock_add_posts_count_in_badges_list: mock add_posts_count_in_badges_list helper method
        :param mock_render_response: mock render_to_response method because we are having problems with our templates
        :return: None
        """
        request = self.request_factory.get(reverse('my_badges', kwargs={'course_id': self.course.id}))
        request.user = self.user

        CourseEnrollmentFactory(user=self.user, course_id=self.course.id, is_active=True)
        DiscussionCommunityFactory(course_id=self.course.id, community_url='100/abc')

        courses_discussion_data = [
            {str(self.course.id): {DISCUSSION_ID_KEY: 100}}
        ]

        badges, sample_api_request, sample_api_response = get_all_data_dicts(self, courses_discussion_data)

        courses_discussion_data[0][str(self.course.id)][DISCUSSION_COUNT_KEY] = 3  # Could be any number

        mock_get_badge_progress_request_data.return_value = sample_api_request
        mock_nodebb_client.return_value.badges.get_progress = mock.MagicMock(
            return_value=(api_status_code, sample_api_response))

        badging_views.my_badges(request, self.course.id)

        mock_nodebb_client.return_value.badges.get_progress.assert_called_once_with(request_data=sample_api_request)

        if api_status_code == STATUS_CODE_TRUE:
            mock_add_posts_count_in_badges_list.assert_called_once_with(sample_api_response[COURSES_KEY][0], badges)
        else:
            self.assertEqual(mock_add_posts_count_in_badges_list.call_count, 0)


def get_all_data_dicts(self, courses_discussion_data):
    badges = {
        CONVERSATIONALIST[CONVERSATIONALIST_ENTRY_INDEX]: []
    }

    sample_api_response = {
        COURSES_KEY: courses_discussion_data
    }

    sample_api_request = {
        USERNAME_KEY: self.user.username,
        COURSES_KEY: json.dumps(sample_api_response)
    }

    return badges, sample_api_request, sample_api_response
