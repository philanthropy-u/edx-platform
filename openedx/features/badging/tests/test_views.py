import mock

from django.core.urlresolvers import reverse
from django.http import Http404
from django.test import RequestFactory
from django.test.client import Client

from openedx.core.djangoapps.xmodule_django.models import CourseKeyField
from student.tests.factories import CourseEnrollmentFactory
from student.tests.factories import UserFactory
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory

from .factories import BadgeFactory, UserBadgeFactory
from .. import views as badging_views


class BadgeViewsTestCases(ModuleStoreTestCase):

    def setUp(self):
        super(BadgeViewsTestCases, self).setUp()
        self.course = CourseFactory(org="test", number="123", run="1")
        self.request_factory = RequestFactory()
        self.user = UserFactory()

    def test_trophycase_with_various_course(self):
        request = self.request_factory.get(reverse('trophycase'))
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
        request = self.request_factory.get(reverse('trophycase'))
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

    def test_my_badges_denies_anonymous(self):
        """This method test API call without logged-in user. In this case user must be redirected
         to login page
        """
        path = reverse('my_badges', kwargs={'course_id': 'course/123/1'})
        response = Client().get(path=path)
        self.assertRedirects(response, '{}?next={}'.format(reverse('signin_user'), path))

    def test_my_badges_invalid_course_id(self):
        course_id = 'test/course/123'
        path = reverse('my_badges', kwargs={'course_id': course_id})

        request = self.request_factory.get(path)
        request.user = self.user

        with self.assertRaises(Http404):
            badging_views.my_badges(request, course_id)

    @mock.patch('openedx.features.badging.views.get_course_badges')
    def test_my_badges_with_enrolled_and_active_course(self, mock_get_course_badges):
        CourseEnrollmentFactory(user=self.user, course_id=self.course.id, is_active=True)

        path = reverse('my_badges', kwargs={'course_id': self.course.id})
        request = self.request_factory.get(path)
        request.user = self.user

        mock_get_course_badges.return_value = dict()
        badging_views.my_badges(request, self.course.id)
        mock_get_course_badges.assert_called_once_with(request.user, self.course.id, list())

    def test_my_badges_with_enrolled_but_inactive_course(self):
        CourseEnrollmentFactory(user=self.user, course_id=self.course.id, is_active=False)

        path = reverse('my_badges', kwargs={'course_id': self.course.id})
        request = self.request_factory.get(path)
        request.user = self.user

        with self.assertRaises(Http404):
            badging_views.my_badges(request, self.course.id)

    @mock.patch('openedx.features.badging.views.get_course_badges')
    def test_my_badges_with_some_earned_badges(self, mock_get_course_badges):
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

