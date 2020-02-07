from mock import patch

from django.test import RequestFactory, TestCase

from student.tests.factories import UserFactory

from lms.djangoapps.onboarding.models import Organization
from openedx.features.student_account.forms import AccountCreationFormCustom
from openedx.features.student_account.helpers import set_opt_in_and_affiliate_user_organization


class SetOptInAndAffiliateOrganizationTests(TestCase):
    def setUp(self):
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
        request = RequestFactory().post('/user_api/v1/account/registration/',
                                        self.request_data)
        params = dict(request.POST.copy().items())
        params['name'] = "{} {}".format(params.get('first_name'), params.get('last_name'))

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

        self.request_data['org_name'] = 'new_organization'
        self.request_data['org_size'] = '5-10'
        self.request_data['org_type'] = 'IWRNS'

        request = RequestFactory().post('/user_api/v1/account/registration/', self.request_data)
        params = dict(request.POST.copy().items())
        params['name'] = "{} {}".format(params.get('first_name'), params.get('last_name'))

        form = AccountCreationFormCustom(data=params,
                                         extended_profile_fields=None,
                                         do_third_party_auth=False)
        form.is_valid()

        set_opt_in_and_affiliate_user_organization(self.user, form)
        created_organization = Organization.objects.filter(label=form.cleaned_data.get("org_name")).first()

        user_extended_profile_data = {
            'is_first_learner': True,
            "organization_id": created_organization.id
        }

        user_extended_profile_create_method.assert_called_once_with(user=self.user, **user_extended_profile_data)
        email_preferences_create_method.assert_called_once_with(user=self.user,
                                                                opt_in=form.cleaned_data.get('opt_in'))

    @patch('openedx.features.student_account.helpers.EmailPreference.objects.create')
    @patch('openedx.features.student_account.helpers.UserExtendedProfile.objects.create')
    def test_user_with_existing_organization(self, user_extended_profile_create_method,
                                             email_preferences_create_method):

        existing_organization = Organization.objects.create(label="existing_organization")
        self.request_data['org_name'] = existing_organization.label

        request = RequestFactory().post('/user_api/v1/account/registration/', self.request_data)
        params = dict(request.POST.copy().items())
        params['name'] = "{} {}".format(params.get('first_name'), params.get('last_name'))

        form = AccountCreationFormCustom(data=params,
                                         extended_profile_fields=None,
                                         do_third_party_auth=False)
        form.is_valid()
        set_opt_in_and_affiliate_user_organization(self.user, form)

        user_extended_profile_data = {
            "organization_id": existing_organization.id
        }

        user_extended_profile_create_method.assert_called_once_with(user=self.user, **user_extended_profile_data)
        email_preferences_create_method.assert_called_once_with(user=self.user,
                                                                opt_in=form.cleaned_data.get('opt_in'))
