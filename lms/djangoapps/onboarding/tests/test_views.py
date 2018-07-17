import unittest

from mock import patch, MagicMock, Mock

import json
import httpretty

from django.conf import settings
from django.core.urlresolvers import reverse
from xmodule.modulestore.tests.django_utils import SharedModuleStoreTestCase

from django.contrib.auth.models import User
from lms.djangoapps.courseware.tests.helpers import LoginEnrollmentTestCase
from lms.djangoapps.onboarding.models import UserExtendedProfile
from lms.djangoapps.onboarding.tests.factories import EnglishProficiencyFactory, EducationLevelFactory, \
    RoleInsideOrgFactory, OrgSectorFactory, OperationLevelFactory, FocusAreaFactory, TotalEmployeeFactory
from openedx.core.djangolib.testing.utils import get_mock_request


@patch.dict(settings.FEATURES, {'BYPASS_ACTIVATION_EMAIL_FOR_EXTAUTH': False, 'AUTOMATIC_AUTH_FOR_TESTING': False, 'SKIP_EMAIL_VALIDATION': True})
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

        patch('nodebb.signals.handlers.send_user_info_to_mailchimp',
              Mock(return_value=MagicMock())).start()

        patch('nodebb.signals.handlers.send_user_profile_info_to_mailchimp',
              Mock(return_value=MagicMock())).start()

        patch('nodebb.signals.handlers.get_current_request',
               Mock(return_value=MagicMock())).start()

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

        for (key, _field) in self.form_data.items():
            if key in ["year_of_birth", "gender", "level_of_education", "language", "city"]:
                self.assertEqual(getattr(user_extended_profile.user.profile, key) , self.form_data[key])
            elif key in ["not_listed_gender", "english_proficiency"]:
                self.assertEqual(getattr(user_extended_profile, key) , self.form_data[key])
            elif key in ["country"]:
                self.assertEqual(getattr(user_extended_profile.user.profile, key).name, self.form_data[key])

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
class TestRegistration(LoginEnrollmentTestCase, SharedModuleStoreTestCase):

    password = "test"

    @classmethod
    def setUpClass(cls):
        super(TestRegistration, cls).setUpClass()

        cls.request = get_mock_request()

        RoleInsideOrgFactory.create(
            code='INTERN',
            label="Intern"
        )
        OrgSectorFactory.create(
            code='IWRNS',
            label="I'd rather not say"
        )
        OperationLevelFactory.create(
            code='IWRNS',
            label="I'd rather not say"
        )
        FocusAreaFactory.create(
            code='IWRNS',
            label="I'd rather not say"
        )
        TotalEmployeeFactory.create(
            code='2-5',
            label="2-5"
        )
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

        patch('nodebb.signals.handlers.send_user_info_to_mailchimp',
              Mock(return_value=MagicMock())).start()

        patch('nodebb.signals.handlers.send_user_profile_info_to_mailchimp',
              Mock(return_value=MagicMock())).start()

        patch('nodebb.signals.handlers.get_current_request',
               Mock(return_value=MagicMock())).start()

    def setUp(self):
        """ Create a course and user, then log in. """

        super(TestRegistration, self).setUp()

        response = self.client.get(reverse('signin_user'))
        self.csrf_token = response.cookies.get("csrftoken")

    @patch.dict(settings.FEATURES, {'BYPASS_ACTIVATION_EMAIL_FOR_EXTAUTH': False, 'AUTOMATIC_AUTH_FOR_TESTING': False, 'SKIP_EMAIL_VALIDATION': True})
    def register_user(self, is_employed, is_admin):
        url = reverse('user_api_registration')

        self.email = 'user@test.com'
        self.password = 'test'
        self.username = 'padfoot'

        form_data = {
            'email': self.email,
            'username': self.username,
            'password': self.password,
            'confirm_password': self.password,
            'first_name': 'Sirius',
            'last_name': 'Black',
            'is_currently_employed': 'false' if is_employed else 'true',
            'organization_name': 'Some Organization' if is_employed else '',
            'is_poc': '1' if is_admin else '0',
            'name': '',
            'level_of_education': '',
            'gender': '',
            'year_of_birth': '',
            'mailing_address': '',
            'goals': '',
            'org_admin_email': '',
            'honor_code': 'true',
            'terms_of_service': 'true',
            'csrfmiddlewaretoken': self.csrf_token.value
        }

        resp = self.client.post(url, data=form_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        data = json.loads(resp.content)
        self.assertEqual(data['success'], True)

        # Check both that the user is created, and inactive
        self.user = User.objects.get(email=self.email)
        self.assertTrue(self.user.is_active)

    def post_user_info_form(self):

        user_info_form_data = {
            'year_of_birth': 1970,
            'gender': 'm',
            'not_listed_gender': '',
            'level_of_education': "BD",
            'language': 'Urdu',
            'english_proficiency': "INT",
            'country': 'Pakistan',
            'city': '',
            'country_of_employment': '',
            'city_of_employment': '',
            'role_in_org': 'INTERN',
            'start_month_year': '07/2018',
            'hours_per_week': '120',
            'csrfmiddlewaretoken': self.csrf_token.value
        }
        resp = self.client.post(self.user_info_url, data=user_info_form_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertRedirects(
            resp,
            '{}'.format(self.interests_url, self.user_info_url)
        )

    def post_interest_form_data(self):
        interests_form_data = {
            'csrfmiddlewaretoken': self.csrf_token.value
        }
        resp = self.client.post(self.interests_url, data=interests_form_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertRedirects(
            resp,
            '{}'.format(self.organization_url, self.interests_url)
        )

    def post_organization_form(self, organization_type, redirection_url):
        organization_form_data = {
            'country': 'Pakistan',
            'city': '',
            'is_org_url_exist': 0,
            'url': '',
            'founding_year': 1990,
            'org_type': organization_type,
            'level_of_operation': 'IWRNS',
            'focus_area': 'IWRNS',
            'total_employees': '2-5',
            'alternate_admin_email': '',
            'removed_org_partners': '',
            'csrfmiddlewaretoken': self.csrf_token.value
        }
        resp = self.client.post(self.organization_url, data=organization_form_data,
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertRedirects(
            resp,
            '{}'.format(reverse(redirection_url), self.organization_url)
        )


@patch.dict(settings.FEATURES, {'BYPASS_ACTIVATION_EMAIL_FOR_EXTAUTH': False, 'AUTOMATIC_AUTH_FOR_TESTING': False, 'SKIP_EMAIL_VALIDATION': True})
@httpretty.activate
@unittest.skipUnless(settings.ROOT_URLCONF == 'lms.urls', 'Test only valid in lms')
class TestOnBoardingSteps(TestRegistration):

    password = "test"

    @classmethod
    def setUpClass(cls):
        super(TestOnBoardingSteps, cls).setUpClass()

    def setUp(self):
        """ Create user, then log in. """

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

    @patch('django.template.loader.get_template', Mock(return_value=MagicMock()))
    @patch('edxmako.shortcuts.lookup_template', Mock(return_value=MagicMock()))
    def test_first_learner_should_not_see_organization_details_page(self):
        self.user_info_url = reverse('user_info')
        self.interests_url = reverse('interests')
        self.organization_url = reverse('organization')

        self.register_user(True, False)

        self.user = self.activate_user(self.email)
        self.login(self.email, self.password)

        self.request.user = self.user

        self.post_user_info_form()

        self.post_interest_form_data()

        self.post_organization_form('IWRNS', 'recommendations')

        user_extended_profile = UserExtendedProfile.objects.get(user_id=self.user.id)

        are_forms_complete = not (bool(user_extended_profile.unattended_surveys(_type='list')))
        self.assertTrue(are_forms_complete)
        self.assertFalse(user_extended_profile.is_organization_admin)
        self.assertTrue(user_extended_profile.is_first_signup_in_org)

        resp = self.client.get(reverse('update_organization'))

        self.assertEquals(403, resp.status_code)

    @patch('django.template.loader.get_template', Mock(return_value=MagicMock()))
    @patch('edxmako.shortcuts.lookup_template', Mock(return_value=MagicMock()))
    def test_admin_should_see_organization_details_page(self):
        self.user_info_url = reverse('user_info')
        self.interests_url = reverse('interests')
        self.organization_url = reverse('organization')

        self.register_user(True, True)

        self.user = self.activate_user(self.email)
        self.login(self.email, self.password)

        self.request.user = self.user

        self.post_user_info_form()

        self.post_interest_form_data()

        self.post_organization_form('IWRNS', 'recommendations')

        user_extended_profile = UserExtendedProfile.objects.get(user_id=self.user.id)

        are_forms_complete = not (bool(user_extended_profile.unattended_surveys(_type='list')))
        self.assertTrue(are_forms_complete)
        self.assertTrue(user_extended_profile.is_organization_admin)
        self.assertTrue(user_extended_profile.is_first_signup_in_org)

        resp = self.client.get(reverse('update_organization'))

        self.assertEquals(200, resp.status_code)
