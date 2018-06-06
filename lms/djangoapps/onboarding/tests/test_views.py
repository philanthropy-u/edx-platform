import unittest

import lxml.html

from django.test import override_settings
from django.conf import settings
from django.core.urlresolvers import reverse
from xmodule.modulestore.tests.django_utils import SharedModuleStoreTestCase

from lms.djangoapps.courseware.tests.helpers import LoginEnrollmentTestCase
from lms.djangoapps.onboarding.models import UserExtendedProfile
from lms.djangoapps.onboarding.tests.factories import EnglishProficiencyFactory, EducationLevelFactory
from openedx.core.djangolib.testing.utils import get_mock_request


@override_settings(COMPREHENSIVE_THEME_DIRS=[settings.PHILU_THEME])
@override_settings(MKTG_URLS={'ROOT': 'https://www.example.com'})
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

    def setUp(self):
        """ Create a course and user, then log in. """

        super(TestUserInfoForm, self).setUp()

        EnglishProficiencyFactory.create(
            code='INT',
            label="Intermediate"
        )
        EducationLevelFactory.create(
            code='BD',
            label="Bachelor's Degree"
        )

        self.setup_user()
        self.request.user = self.user

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

        csrf_token = response.cookies.get("csrftoken")
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
            'csrfmiddlewaretoken': csrf_token.value
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

    def test_csrf_token_is_present_in_form(self):
        # Expected html:
        # <form>
        #   ...
        #   <fieldset>
        #       ...
        #       <input name="csrfmiddlewaretoken" value="...">
        #       ...
        #       </fieldset>
        #       ...
        # </form>

        self.client.login(username=self.user.username, password=self.password)

        response = self.client.get(reverse('user_info'))

        csrf_token = response.cookies.get("csrftoken")
        doc = lxml.html.fromstring(response.content)
        form = doc.find_class('survey-form')[0]
        csrf_input_field = form.find(".//input[@name='csrfmiddlewaretoken']")

        self.assertIsNotNone(csrf_token)
        self.assertIsNotNone(csrf_token.value)
        self.assertIsNotNone(csrf_input_field)
        self.assertEqual(csrf_token.value, csrf_input_field.attrib["value"])

        self.client.logout()

    def test_happy_path_post_request(self):

        url = reverse('user_info')

        response = self.client.get(url, follow=True)

        csrf_token = response.cookies.get("csrftoken")
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
            'csrfmiddlewaretoken': csrf_token.value
        }

        resp = self.client.post(url, data=self.form_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        user_extended_profile = UserExtendedProfile.objects.get(user_id=self.request.user.id)

        self.assertEqual(user_extended_profile.user.profile.year_of_birth, self.form_data["year_of_birth"])
        self.assertEqual(user_extended_profile.user.profile.gender, self.form_data["gender"])
        self.assertEqual(user_extended_profile.not_listed_gender, self.form_data["not_listed_gender"])
        self.assertEqual(user_extended_profile.user.profile.level_of_education, self.form_data["level_of_education"])
        self.assertEqual(user_extended_profile.user.profile.language, self.form_data["language"])
        self.assertEqual(user_extended_profile.english_proficiency, self.form_data["english_proficiency"])
        self.assertEqual(user_extended_profile.user.profile.country.name, self.form_data["country"])
        self.assertEqual(user_extended_profile.user.profile.city, self.form_data["city"])

        self.assertRedirects(
            resp,
            '{}'.format(reverse('interests'), url)
        )

    def test_fail_path_post_request(self):
        response = self.client.get(reverse('user_info'), follow=True)

        csrf_token = response.cookies.get("csrftoken")
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
            'csrfmiddlewaretoken': csrf_token.value
        }

        resp = self.client.post(reverse('user_info'), self.form_data)

        user_extended_profile = UserExtendedProfile.objects.get(user_id=self.request.user.id)

        # assert that data is not saved
        self.assertNotEqual(user_extended_profile.user.profile.year_of_birth, self.form_data["year_of_birth"])
        self.assertNotEqual(user_extended_profile.user.profile.gender, self.form_data["gender"])

        self.assertEqual(resp.status_code, 200)

    def test_age_less_than_eighteen(self):
        response = self.client.get(reverse('user_info'), follow=True)

        csrf_token = response.cookies.get("csrftoken")
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
            'csrfmiddlewaretoken': csrf_token.value
        }

        resp = self.client.post(reverse('user_info'), self.form_data)

        doc = lxml.html.fromstring(resp.content)
        alert_dialog = doc.get_element_by_id('dialog-confirm')

        self.assertEqual("Delete your account", alert_dialog.attrib["title"])
