from django.test import RequestFactory, TestCase

from student.tests.factories import RegistrationFactory, UserFactory

from openedx.features.student_account.helpers import save_user_utm_info
from openedx.features.user_leads.models import UserLeads


class SaveUserUTMInfoTests(TestCase):
    """
    The purpose of this test suite is to ensure that the save_user_utm_info
    helper always works, no matter if the user provides all, partial or no
    utm parameters.
    """

    def setUp(self):
        """
        Create a user object using UserFactory for each test case
        """

        self.user = UserFactory.create()

    def test_save_utm_normal(self):
        """
        Create sample utm parameters data, pass it as POST request parameters
        and assert that the UserLeads object created has all the same values
        as were passed in the request.
        """

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
        """
        Create a request with no UTM params and assert that the UserLeads
        object created is the database is None
        """

        request = RequestFactory().post(
            '/user_api/v1/account/registration/'
        )

        save_user_utm_info(request, self.user)
        saved_utm = UserLeads.objects.filter(user=self.user).first()
        assert saved_utm is None

    def test_save_utm_no_request(self):
        """
        Ensure that sending None as a request to the save_user_utm_info
        method throws an exception
        """

        request = None
        save_user_utm_info(request, self.user)
        self.assertRaises(Exception)

