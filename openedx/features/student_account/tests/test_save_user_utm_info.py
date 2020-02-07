from django.test import RequestFactory, TestCase

from student.tests.factories import RegistrationFactory, UserFactory

from openedx.features.student_account.helpers import save_user_utm_info
from openedx.features.user_leads.models import UserLeads


class SaveUserUTMInfoTests(TestCase):
    def setUp(self):
        self.user = UserFactory.create()

    def test_save_utm_normal(self):
        utm_data_to_save = {
            'utm_source': 'testSource1',
            'utm_medium': 'testMedium',
            'utm_campaign': 'testCampaign',
            'utm_content': 'testContent',
            'utm_term': 'testTerm'
        }

        request = RequestFactory().post(
            '/user_api/v1/account/registration/', utm_data_to_save
        )

        save_user_utm_info(request, self.user)
        saved_utm = UserLeads.objects.filter(user=self.user).values(*utm_data_to_save.keys()).first()
        self.assertDictEqual(saved_utm, utm_data_to_save)

    def test_save_utm_empty(self):
        request = RequestFactory().post(
            '/user_api/v1/account/registration/'
        )

        save_user_utm_info(request, self.user)
        saved_utm = UserLeads.objects.filter(user=self.user).first()
        assert saved_utm is None

    def test_save_utm_no_request(self):
        request = None
        save_user_utm_info(request, self.user)
        self.assertRaises(Exception)

