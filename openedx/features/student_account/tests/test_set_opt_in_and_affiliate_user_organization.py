from mock import patch

from django.test import RequestFactory, TestCase

from student.tests.factories import UserFactory

from lms.djangoapps.onboarding.models import Organization
from openedx.features.student_account.forms import AccountCreationFormCustom
from openedx.features.student_account.helpers import set_opt_in_and_affiliate_user_organization


class SetOptInAndAffiliateOrganizationTests(TestCase):
    """
    The purpose of this test suite is to check if the set_opt_in_and_affiliate_user_organization
    method is working for both affiliated and unaffiliated users. Also, that the user is affiliated
    with the existing organization or a new organization is created and the user is the first learner.

    This suite also tests that the email preferences model object for the user is created.
    """

    def setUp(self):
        """
        Create a dictionary containing the request data for user registration for
        each test case. This dictionary is modified by inserting new keys depending
        on the test case.

        Also create a user type object using UserFactory, for each new test case.
        """

        self.request_data = {
            'email': 'testUser@example.com',
            'username': 'testUser',
            'password': 'Edx123',
            'first_name': 'Test',
            'last_name': 'User',
            'honor_code': 'true',
            'opt_in': 'yes',
        }
        self.user = UserFactory.create()

    @patch('openedx.features.student_account.helpers.Organization.objects.get_or_create')
    @patch('openedx.features.student_account.helpers.EmailPreference.objects.create')
    @patch('openedx.features.student_account.helpers.UserExtendedProfile.objects.create')
    def test_unaffiliated_user(self, user_extended_profile_create_method,
                               email_preferences_create_method, org_get_or_create_method):
        """
        Test that when no organization related data is present in the request, the
        form cleans the data without raising any validation errors, passes the
        data to set_opt_in_and_affiliate_user_organization method, does not
        fetch an existing organization or create a new organization,
        and then saves the UserExtendedProfile and EmailPreferences
        """

        request = RequestFactory().post('/user_api/v1/account/registration/',
                                        self.request_data)
        params = dict(request.POST.copy().items())
        params['name'] = '{} {}'.format(params.get('first_name'), params.get('last_name'))

        form = AccountCreationFormCustom(data=params,
                                         extended_profile_fields=None,
                                         do_third_party_auth=False)
        form.is_valid()
        set_opt_in_and_affiliate_user_organization(self.user, form)

        org_get_or_create_method.assert_not_called()
        user_extended_profile_create_method.assert_called_once_with(user=self.user, **{})
        email_preferences_create_method.assert_called_once_with(user=self.user, opt_in=form.cleaned_data.get('opt_in'))

    @patch('openedx.features.student_account.helpers.EmailPreference.objects.create')
    @patch('openedx.features.student_account.helpers.UserExtendedProfile.objects.create')
    def test_user_with_new_organization(self, user_extended_profile_create_method, email_preferences_create_method):
        """
        Test that when the user gives a new organization fields in the request,
        the form does not raise any validation error.

        A new organization is created, and the user is made first_learner for that
        organization in the UserExtendedProfile and the EmailPreferences are
        also set for that user
        """

        self.request_data['org_name'] = 'new_organization'
        self.request_data['org_size'] = '5-10'
        self.request_data['org_type'] = 'IWRNS'

        request = RequestFactory().post('/user_api/v1/account/registration/', self.request_data)
        params = dict(request.POST.copy().items())
        params['name'] = '{} {}'.format(params.get('first_name'), params.get('last_name'))

        form = AccountCreationFormCustom(data=params,
                                         extended_profile_fields=None,
                                         do_third_party_auth=False)
        form.is_valid()

        set_opt_in_and_affiliate_user_organization(self.user, form)
        created_organization = Organization.objects.filter(label=form.cleaned_data.get('org_name')).first()

        user_extended_profile_data = {
            'is_first_learner': True,
            'organization_id': created_organization.id
        }

        user_extended_profile_create_method.assert_called_once_with(user=self.user, **user_extended_profile_data)
        email_preferences_create_method.assert_called_once_with(user=self.user,
                                                                opt_in=form.cleaned_data.get('opt_in'))

    @patch('openedx.features.student_account.helpers.EmailPreference.objects.create')
    @patch('openedx.features.student_account.helpers.UserExtendedProfile.objects.create')
    def test_user_with_existing_organization(self, user_extended_profile_create_method,
                                             email_preferences_create_method):
        """
        Test that when a user gives the name of an already existing organization,
        they are affiliated with that organization. The form does not raise any validation
        errors, the EmailPreferences are also set for that user.
        """

        existing_organization = Organization.objects.create(label='existing_organization')
        self.request_data['org_name'] = existing_organization.label

        request = RequestFactory().post('/user_api/v1/account/registration/', self.request_data)
        params = dict(request.POST.copy().items())
        params['name'] = '{} {}'.format(params.get('first_name'), params.get('last_name'))

        form = AccountCreationFormCustom(data=params,
                                         extended_profile_fields=None,
                                         do_third_party_auth=False)
        form.is_valid()
        set_opt_in_and_affiliate_user_organization(self.user, form)

        user_extended_profile_data = {
            'organization_id': existing_organization.id
        }

        user_extended_profile_create_method.assert_called_once_with(user=self.user, **user_extended_profile_data)
        email_preferences_create_method.assert_called_once_with(user=self.user,
                                                                opt_in=form.cleaned_data.get('opt_in'))
