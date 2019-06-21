import urllib

import mock
import factory
from django.conf import settings
from django.db.models import signals
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import modify_settings, override_settings
from django.contrib.sites.models import Site
from w3lib.url import add_or_replace_parameter

from openedx.core.djangoapps.theming.models import SiteTheme
from lms.djangoapps.teams.tests.factories import CourseTeamMembershipFactory
from lms.djangoapps.onboarding.tests.factories import UserFactory
from student.tests.factories import CourseEnrollmentFactory
from xmodule.modulestore.tests.factories import CourseFactory
from xmodule.modulestore import ModuleStoreEnum
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase

from openedx.features.teams.serializers import CustomCourseTeamCreationSerializer
from openedx.features.teams.tests.factories import CourseTeamFactory



NONE_EXISTING_TEAM_ID = 'team-not-exists'
INVALID_TOPIC_PATTERN = 'invalid'
INVALID_TOPIC_ID = '-1'
TEST_TOPIC_URL = '/topic/test-1'

TEST_USERNAME = 'test_user'
TEST_PASSWORD = 'test_password'


@factory.django.mute_signals(signals.pre_save, signals.post_save)
@override_settings(MIDDLEWARE_CLASSES=[klass for klass in settings.MIDDLEWARE_CLASSES if klass != 'lms.djangoapps.onboarding.middleware.RedirectMiddleware'])
class TeamsTestsBaseClass(ModuleStoreTestCase):

    @classmethod
    def setUpClass(cls):
        super(TeamsTestsBaseClass, cls).setUpClass()
        site = Site(domain='testserver', name='test')
        site.save()
        theme = SiteTheme(site=site, theme_dir_name='philu')
        theme.save()


    def setUp(self):
        super(TeamsTestsBaseClass, self).setUp()
        self.topic = self._create_topic()
        self.course = self._create_course()
        self.team = self._create_team(self.course)
        self.user = self._create_user()
        self._create_team_membership(self.team, self.user)
        self._initiate_urls()

    def _create_topic(self):
        topic = {u'name': u'T0pic', u'description': u'The best topic!', u'id': u'0', 'url': 'example.com/topic/0'}
        return topic

    def _create_course(self, **kwargs):
        org = kwargs.get('org') or 'edX'
        course_number = kwargs.get('course_number') or 'CS101'
        course_run = kwargs.get('course_run') or '2015_Q1'
        display_name = kwargs.get('display_name') or 'test course 1'
        course = CourseFactory.create(
            org=org,
            number=course_number,
            run=course_run,
            display_name=display_name,
            default_store=ModuleStoreEnum.Type.split,
            teams_configuration={
                "max_team_size": 10,
                "topics": [self.topic]
            }
        )
        return course

    def _create_team(self, course):
        team = CourseTeamFactory.create(
            course_id=course.id,
            topic_id=course.teams_topics[0]['id'],
            name='Test Team',
            description='Testing Testing Testing...',
        )
        return team

    def _create_user(self, username=TEST_USERNAME, password=TEST_PASSWORD, **kwargs):
        user = UserFactory.create(username= username, password=password, **kwargs)
        return user

    def _create_team_membership(self, team, user):
        membership = CourseTeamMembershipFactory.create(team=team, user=user)
        return membership

    def _enroll_user_in_course(self, user, course_id):
        enrollment= CourseEnrollmentFactory(user=user, course_id=course_id)
        return enrollment

    def _initiate_urls(self):
        self.teams_dashboard_url = reverse('teams_dashboard', args=[self.course.id])
        self.topic_teams_url = reverse('browse_topic_teams', args=[self.course.id, self.topic['id']])
        self.create_team_url = reverse('create_team', args=[self.course.id, self.topic['id']])
        self.my_team_url = reverse('my_team', args=[self.course.id])
        self.view_team_url = reverse('view_team', args=[self.course.id, self.team.team_id])
        self.team_update_url = reverse('update_team', args=[self.course.id, self.team.team_id])
        self.team_edit_membership_url = reverse('edit_team_memberships', args=[self.course.id, self.team.team_id])


class BrowseTeamsTestCase(TeamsTestsBaseClass):

    def test_anonymous(self):
        """Verifies that an anonymous client cannot access the team
        dashboard, and is redirected to the login page."""
        anonymous_client = Client()
        response = anonymous_client.get(self.teams_dashboard_url)
        redirect_url = '{0}?next={1}'.format(settings.LOGIN_URL, urllib.quote(self.teams_dashboard_url))
        self.assertRedirects(response, redirect_url)

    @mock.patch.dict("django.conf.settings.FEATURES", {'ENABLE_TEAMS': False})
    def test_404_feature_disabled(self):
        client = Client()
        client.login(username=self.user.username, password=TEST_PASSWORD)
        response = client.get(self.teams_dashboard_url, follow=False)
        # TODO: BUG: raise http404
        # self.assertEqual(404, response.status_code)
        # status code 302 is because there is a matching url pattern for generated 404 url.
        redirect_url = '{}404/'.format(self.teams_dashboard_url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=302)

    def test_404_not_enrolled_not_staff(self):
        client = Client()
        client.login(username=self.user.username, password=TEST_PASSWORD)
        response = client.get(self.teams_dashboard_url, follow=False)
        # TODO: BUG: raise http404
        # self.assertEqual(404, response.status_code)
        redirect_url = '{}404/'.format(self.teams_dashboard_url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=302)

    def test_not_enrolled_staff(self):
        client = Client()
        staff_user = self._create_user(username='staff_test_user', is_staff=True)
        client.login(username=staff_user.username, password=TEST_PASSWORD)
        response = client.get(self.teams_dashboard_url)
        # TODO: WHAT TO TEST IN RESPONSE
        self.assertEqual(200, response.status_code)

    def test_enrolled_not_staff(self):
        client = Client()
        self._enroll_user_in_course(user=self.user, course_id=self.course.id)
        client.login(username=self.user.username, password=TEST_PASSWORD)
        response = client.get(self.teams_dashboard_url)
        # TODO: WHAT TO TEST IN RESPONSE
        self.assertEqual(200, response.status_code)

    def test_enrolled_staff_browse_teams(self):
        client = Client()
        staff_user = self._create_user(username='staff_test_user', is_staff=True)
        enrolled_user = self._enroll_user_in_course(user=staff_user, course_id=self.course.id)
        client.login(username=staff_user.username, password=TEST_PASSWORD)
        response = client.get(self.teams_dashboard_url)
        # TODO: WHAT TO TEST IN RESPONSE
        self.assertEqual(200, response.status_code)


class BrowseTopicTeamsTestCase(TeamsTestsBaseClass):

    def test_anonymous(self):
        """Verifies that an anonymous client cannot access the team
        topics, and is redirected to the login page."""

        anonymous_client = Client()
        response = anonymous_client.get(self.topic_teams_url)
        redirect_url = '{0}?next={1}'.format(settings.LOGIN_URL, urllib.quote(self.topic_teams_url))
        self.assertRedirects(response, redirect_url)

    def test_404_invalid_topic_id(self):
        client = Client()
        client.login(username=self.user.username, password=TEST_PASSWORD)
        invalid_topic_teams_url = reverse('browse_topic_teams', args=[self.course.id, INVALID_TOPIC_PATTERN])
        response = client.get(invalid_topic_teams_url, follow=False)
        # TODO: BUG: raise http404
        # self.assertEqual(404, response.status_code)
        redirect_url = '{}404/'.format(invalid_topic_teams_url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=404)

    def test_browse_topic_teams(self):
        client = Client()
        client.login(username=self.user.username, password=TEST_PASSWORD)
        response = client.get(self.topic_teams_url)
        # TODO: WHAT TO TEST IN RESPONSE
        self.assertEqual(200, response.status_code)


class CreateTeamTestCase(TeamsTestsBaseClass):

    def test_anonymous(self):
        """Verifies that an anonymous client cannot access the team
        topics, and is redirected to the login page."""

        anonymous_client = Client()
        response = anonymous_client.get(self.create_team_url)
        redirect_url = '{0}?next={1}'.format(settings.LOGIN_URL, urllib.quote(self.create_team_url))
        self.assertRedirects(response, redirect_url)

    def test_404_invalid_topic(self):
        client = Client()
        client.login(username=self.user.username, password=TEST_PASSWORD)
        invalid_team_create_url = reverse('create_team', args=[self.course.id, INVALID_TOPIC_ID])
        response = client.get(invalid_team_create_url, follow=False)
        # TODO: BUG: raise http404
        # self.assertEqual(404, response.status_code)
        redirect_url = '{}404/'.format(invalid_team_create_url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=404)

    def test_create_team(self):
        client = Client()
        client.login(username=self.user.username, password=TEST_PASSWORD)
        response = client.get(self.create_team_url)
        # TODO: WHAT TO TEST IN RESPONSE
        self.assertEqual(200, response.status_code)


class MyTeamTestCase(TeamsTestsBaseClass):

    def test_anonymous(self):
        """Verifies that an anonymous client cannot access the team
        topics, and is redirected to the login page."""

        anonymous_client = Client()
        response = anonymous_client.get(self.my_team_url)
        redirect_url = '{0}?next={1}'.format(settings.LOGIN_URL, urllib.quote(self.my_team_url))
        self.assertRedirects(response, redirect_url)

    def test_no_course_team_exists(self):
        """Test the ok response when there is no team for givne course id.
        """
        client = Client()
        client.login(username=self.user.username, password=TEST_PASSWORD)
        # Have to different course number to avoid duplicate course-key error due to already existing self.course
        # with same data
        course_with_no_teams = self._create_course(course_number='CS-102')
        url = reverse('my_team', args=[course_with_no_teams.id])
        response = client.get(url)
        # TODO: WHAT TO TEST IN RESPONSE
        self.assertEqual(200, response.status_code)

    def test_course_team_exists_no_topic_url(self):
        client = Client()
        client.login(username=self.user.username, password=TEST_PASSWORD)
        response = client.get(self.my_team_url, follow=False)
        redirect_url = self.view_team_url
        self.assertRedirects(response, redirect_url)

    def test_course_team_exists_topic_url(self):
        client = Client()
        client.login(username=self.user.username, password=TEST_PASSWORD)

        response = client.get(self.my_team_url, {'topic_url': TEST_TOPIC_URL}, follow=False)

        redirect_url = self.view_team_url
        redirect_url = add_or_replace_parameter(redirect_url, 'topic_url', TEST_TOPIC_URL)

        self.assertRedirects(response, redirect_url)


class ViewTeamTestCase(TeamsTestsBaseClass):

    def test_anonymous(self):
        """Verifies that an anonymous client cannot access the team
        topics, and is redirected to the login page."""

        anonymous_client = Client()
        response = anonymous_client.get(self.my_team_url)
        redirect_url = '{0}?next={1}'.format(settings.LOGIN_URL, urllib.quote(self.my_team_url))
        self.assertRedirects(response, redirect_url)

    def test_404_no_team_exists(self):
        client = Client()
        url = reverse('view_team', args=[self.course.id, NONE_EXISTING_TEAM_ID])
        client.login(username=self.user.username, password=TEST_PASSWORD)
        response = client.get(url, follow=False)
        # TODO: BUG: raise http404
        # self.assertEqual(404, response.status_code)
        # redirect_url = '{}/404/'.format(url)
        # In this case raise http404 not redirects as in others.
        redirect_url = '{}/'.format(reverse('view_team', args=[self.course.id, 404]))
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=404)

    def test_404_team_no_team_group_chat(self):
        client = Client()
        team_without_group_chat = self._create_team(self.course)
        team_without_group_chat.team.all().delete()
        url = reverse('view_team', args=[self.course.id, team_without_group_chat.team_id])
        client.login(username=self.user.username, password=TEST_PASSWORD)
        response = client.get(url, follow=False)
        # TODO: BUG: raise http404
        # self.assertEqual(404, response.status_code)
        # redirect_url = '{}/404/'.format(url)
        # In this case raise http404 not redirects as in others.
        redirect_url = '{}/'.format(reverse('view_team', args=[self.course.id, 404]))
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=404)

    def test_team_group_chat_team(self):
        client = Client()
        client.login(username=self.user.username, password=TEST_PASSWORD)
        response = client.get(self.view_team_url, follow=False)
        # TODO: WHAT TO TEST IN RESPONSE
        self.assertEqual(response.status_code, 200)


class UpdateTeamTestCase(TeamsTestsBaseClass):

    def test_anonymous(self):
        """Verifies that an anonymous client cannot access the team
        topics, and is redirected to the login page."""

        anonymous_client = Client()
        response = anonymous_client.get(self.team_update_url)
        redirect_url = '{0}?next={1}'.format(settings.LOGIN_URL, urllib.quote(self.team_update_url))
        self.assertRedirects(response, redirect_url)

    def test_404_no_staff(self):
        client = Client()
        client.login(username=self.user.username, password=TEST_PASSWORD)
        response = client.get(self.team_update_url, follow=False)
        # TODO: BUG: raise http404
        # self.assertEqual(404, response.status_code)
        redirect_url = '{}404/'.format(self.team_update_url)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 404)

    def test_404_staff_no_team(self):
        client = Client()
        client.login(username=self.user.username, password=TEST_PASSWORD)
        url = reverse('update_team', args=[self.course.id, NONE_EXISTING_TEAM_ID])
        response = client.get(url, follow=False)
        # TODO: BUG: raise http404
        # self.assertEqual(404, response.status_code)
        redirect_url = '{}404/'.format(url)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 404)

    def test_staff_team_update(self):
        client = Client()
        staff_user = self._create_user(username='staff_test_user', is_staff=True)
        client.login(username=staff_user.username, password=TEST_PASSWORD)
        response = client.get(self.team_update_url)
        self.assertEqual(response.status_code, 200)


class EditTeamMembershitTestCase(TeamsTestsBaseClass):
    def test_anonymous(self):
        """Verifies that an anonymous client cannot access the team
        topics, and is redirected to the login page."""

        anonymous_client = Client()
        response = anonymous_client.get(self.team_edit_membership_url)
        redirect_url = '{0}?next={1}'.format(settings.LOGIN_URL, urllib.quote(self.team_edit_membership_url))
        self.assertRedirects(response, redirect_url)

    def test_404_no_staff(self):
        client = Client()
        client.login(username = self.user.username, password=TEST_PASSWORD)
        response = client.get(self.team_edit_membership_url, follow=False)
        # TODO: BUG: raise http404
        # self.assertEqual(404, response.status_code)
        redirect_url = '{}404/'.format(self.team_edit_membership_url)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 404)

    def test_404_staff_no_team(self):
        client = Client()
        staff_user = self._create_user(username='staff_test_user', is_staff=True)
        client.login(username=staff_user.username, password=TEST_PASSWORD)
        url = reverse('edit_team_memberships', args=[self.course.id, NONE_EXISTING_TEAM_ID])
        response = client.get(url, follow=False)
        # TODO: BUG: raise http404
        # self.assertEqual(404, response.status_code)
        redirect_url = '{}404/'.format(url)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 404)

    def test_staff_team(self):
        client = Client()
        staff_user = self._create_user(username='staff_test_user', is_staff=True)
        client.login(username=staff_user.username, password=TEST_PASSWORD)
        response = client.get(self.team_edit_membership_url, follow=False)
        # TODO: WHAT TO TEST IN RESPONSE
        self.assertEqual(response.status_code, 200)
