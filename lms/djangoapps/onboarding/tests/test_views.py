import unittest

from mock import patch, MagicMock, Mock

import httpretty

from django.conf import settings
from django.core.urlresolvers import reverse
from xmodule.modulestore.tests.django_utils import SharedModuleStoreTestCase

from lms.djangoapps.courseware.tests.helpers import LoginEnrollmentTestCase
from lms.djangoapps.onboarding.models import UserExtendedProfile
from lms.djangoapps.onboarding.tests.factories import EnglishProficiencyFactory, EducationLevelFactory
from openedx.core.djangolib.testing.utils import get_mock_request


@httpretty.activate
@unittest.skipUnless(settings.ROOT_URLCONF == 'lms.urls', 'Test only valid in lms')
class TestUserInfoForm(LoginEnrollmentTestCase, SharedModuleStoreTestCase):
    """
    Test to get user info form
    """

    password = "test"

    @classmethod
    def setUpClass(cls):
        super(TestUserInfoForm, cls).setUpClass()

        cls.request = get_mock_request()

        EnglishProficiencyFactory.create(
            code='INT',
            label="Intermediate"
        )
        EducationLevelFactory.create(
            code='BD',
            label="Bachelor's Degree"
        )

        def create_or_update_user_profile_on_nodebb_mock(self, username, **kwargs):
            return 200, "Success"

        def activate_user_profile_on_nodebb_mock(self, username, active, **kwargs):
            return 200, "Success"

        patch('common.lib.nodebb_client.client.ForumUser.create',
              create_or_update_user_profile_on_nodebb_mock).start()

        patch('common.lib.nodebb_client.client.ForumUser.update_profile',
              create_or_update_user_profile_on_nodebb_mock).start()

        patch('common.lib.nodebb_client.client.ForumUser.activate',
              activate_user_profile_on_nodebb_mock).start()

    def setUp(self):
        """ Create a course and user, then log in. """

        super(TestUserInfoForm, self).setUp()

        url = reverse('signin_user')

        response = self.client.get(url)

        self.csrf_token = response.cookies.get("csrftoken")

        self.setup_user()
        self.request.user = self.user

        def template_loader_mock(template_name, dirs=None, using=None):
            return MagicMock()

        patch('django.template.loader.get_template',
              template_loader_mock).start()

    def test_login_required_get_request(self):
        """
        Verify that login is required to access the page.
        """
        self.client.logout()

        url = reverse('user_info')

        response = self.client.get(url)
        self.assertRedirects(
            response,
            '{}?next={}'.format(reverse('signin_user'), url)
        )

        self.client.login(username=self.user.username, password=self.password)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.client.logout()

    def test_login_required_post_request(self):
        self.client.logout()

        url = reverse('user_info')

        response = self.client.get(url, follow=True)

        assert response.status_code == 200

        self.form_data = {
            'year_of_birth': 1970,
            'gender': 'm',
            'not_listed_gender': '',
            'level_of_education': 'IWRNS',
            'language': 'Urdu',
            'english_proficiency': 'INT',
            'country': 'Pakistan',
            'city': 'Lahore, Pakistan',
            'csrfmiddlewaretoken': self.csrf_token.value
        }

        response = self.client.post(url, self.form_data)
        self.assertRedirects(
            response,
            '{}?next={}'.format(reverse('signin_user'), url)
        )

    def test_redirect_to_onboarding_when_access_other_page(self):
        self.client.login(username=self.user.username, password=self.user.password)

        url = reverse('dashboard')

        response = self.client.get(url)
        self.assertRedirects(
            response,
            '{}'.format(reverse('user_info'), url)
        )

        self.client.logout()

    def test_happy_path_post_request(self):
        url = reverse('user_info')

        response = self.client.get(url, follow=True)

        assert response.status_code == 200

        self.form_data = {
            'year_of_birth': 1970,
            'gender': 'm',
            'not_listed_gender': '',
            'level_of_education': "BD",
            'language': 'Urdu',
            'english_proficiency': "INT",
            'country': 'Pakistan',
            'city': 'Lahore, Pakistan',
            'csrfmiddlewaretoken': self.csrf_token.value
        }

        resp = self.client.post(url, data=self.form_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        user_extended_profile = UserExtendedProfile.objects.get(user_id=self.request.user.id)

        for (_key, field) in self.form_data.items():
            if _key in ["year_of_birth", "gender", "level_of_education", "language", "city"]:
                self.assertEqual(getattr(user_extended_profile.user.profile, _key) , self.form_data[_key])
            elif _key in ["not_listed_gender", "english_proficiency"]:
                self.assertEqual(getattr(user_extended_profile, _key) , self.form_data[_key])
            elif _key in ["country"]:
                self.assertEqual(getattr(user_extended_profile.user.profile, _key).name, self.form_data[_key])

        self.assertRedirects(
            resp,
            '{}'.format(reverse('interests'), url)
        )

    def test_fail_path_post_request(self):
        response = self.client.get(reverse('user_info'), follow=True)

        assert response.status_code == 200

        self.form_data = {
            'year_of_birth': 1970,
            'gender': 'm',
            'not_listed_gender': '',
            'level_of_education': '',
            'language': '',
            'english_proficiency': '',
            'country': '',
            'city': '',
            'csrfmiddlewaretoken': self.csrf_token.value
        }

        resp = self.client.post(reverse('user_info'), self.form_data)

        user_extended_profile = UserExtendedProfile.objects.get(user_id=self.request.user.id)

        # assert that data is not saved
        self.assertNotEqual(user_extended_profile.user.profile.year_of_birth, self.form_data["year_of_birth"])
        self.assertNotEqual(user_extended_profile.user.profile.gender, self.form_data["gender"])

        self.assertEqual(resp.status_code, 200)

    def test_age_less_than_eighteen(self):
        response = self.client.get(reverse('user_info'), follow=True)

        assert response.status_code == 200

        self.form_data = {
            'year_of_birth': 2017,
            'gender': 'm',
            'not_listed_gender': '',
            'level_of_education': "BD",
            'language': 'Urdu',
            'english_proficiency': "INT",
            'country': 'Pakistan',
            'city': 'Lahore, Pakistan',
            'csrfmiddlewaretoken': self.csrf_token.value
        }

        resp = self.client.post(reverse('user_info'), self.form_data)

        user_extended_profile = UserExtendedProfile.objects.get(user_id=self.request.user.id)

        # assert that data is not saved
        self.assertNotEqual(user_extended_profile.user.profile.year_of_birth, self.form_data["year_of_birth"])
        self.assertNotEqual(user_extended_profile.user.profile.gender, self.form_data["gender"])

        self.assertEqual(resp.status_code, 200)


@httpretty.activate
@unittest.skipUnless(settings.ROOT_URLCONF == 'lms.urls', 'Test only valid in lms')
class TestOnBoardingSteps(LoginEnrollmentTestCase, SharedModuleStoreTestCase):


    password = "test"

    @classmethod
    def setUpClass(cls):
        super(TestOnBoardingSteps, cls).setUpClass()

        cls.request = get_mock_request()

        EnglishProficiencyFactory.create(
            code='INT',
            label="Intermediate"
        )
        EducationLevelFactory.create(
            code='BD',
            label="Bachelor's Degree"
        )

        def create_or_update_user_profile_on_nodebb_mock(self, username, **kwargs):
            return 200, "Success"

        def activate_user_profile_on_nodebb_mock(self, username, active, **kwargs):
            return 200, "Success"

        def update_onboarding_surveys_status_mock(self, username):
            return 200, "Success"

        def get_joined_communities_mock(self, username, **kwargs):
            return 200, []

        patch('common.lib.nodebb_client.client.ForumUser.create',
              create_or_update_user_profile_on_nodebb_mock).start()

        patch('common.lib.nodebb_client.client.ForumUser.update_profile',
              create_or_update_user_profile_on_nodebb_mock).start()

        patch('common.lib.nodebb_client.client.ForumUser.activate',
              activate_user_profile_on_nodebb_mock).start()

        patch('common.lib.nodebb_client.client.ForumUser.update_onboarding_surveys_status',
              update_onboarding_surveys_status_mock).start()

        patch('common.lib.nodebb_client.client.ForumCategory.joined',
              get_joined_communities_mock).start()

    def setUp(self):
        """ Create a course and user, then log in. """

        super(TestOnBoardingSteps, self).setUp()

        url = reverse('signin_user')

        response = self.client.get(url)

        self.csrf_token = response.cookies.get("csrftoken")

        self.setup_user('false')
        self.request.user = self.user

    @patch('django.template.loader.get_template', Mock(return_value=MagicMock()))
    @patch('edxmako.shortcuts.lookup_template', Mock(return_value=MagicMock()))
    def test_unemployed_should_be_redirected_to_dashboard_after_second_step(self):
        user_info_url = reverse('user_info')
        interests_url = reverse('interests')

        self.form_data = {
            'year_of_birth': 1970,
            'gender': 'm',
            'not_listed_gender': '',
            'level_of_education': "BD",
            'language': 'Urdu',
            'english_proficiency': "INT",
            'country': 'Pakistan',
            'city': 'Lahore, Pakistan',
            'csrfmiddlewaretoken': self.csrf_token.value
        }

        resp = self.client.post(user_info_url, data=self.form_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertRedirects(
            resp,
            '{}'.format(interests_url, user_info_url)
        )

        self.interests_form_data = {
            'csrfmiddlewaretoken': self.csrf_token.value
        }

        resp = self.client.post(interests_url, data=self.interests_form_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertRedirects(
            resp,
            '{}'.format(reverse('recommendations'), interests_url)
        )
