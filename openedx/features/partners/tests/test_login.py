from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from openedx.features.partners.tests.factories import PartnerUserFactory, PartnerFactory
from student.tests.factories import UserFactory


class LoginTestCases(APITestCase):

    def setUp(self):
        self.partner_login_end_point = reverse('partner_login', args=['give2asia'])
        self.user = UserFactory(password='Abc12345')

    def test_login_with_correct_credentials(self):
        """
        Testing login with valid credentials, i.e, The email is registered and correct password is provided
        """
        valid_data = {
            'email': self.user.email,
            'password': self.user.password
        }

        partner = PartnerFactory(slug='give2asia')

        PartnerUserFactory(user_id=self.user.id, partner_id=partner.id)

        response = self.client.post(
            self.partner_login_end_point,
            data=valid_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_incorrect_password(self):
        """
        Providing incorrect password
        """
        invalid_data = {
            'email': self.user.email,
            'password': 'incorrectpassword'
        }
        partner = PartnerFactory(slug='give2asia')

        PartnerUserFactory(user_id=self.user.id, partner_id=partner.id)

        response = self.client.post(
            self.partner_login_end_point,
            data=invalid_data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_with_not_registered_username(self):
        """
        Providing username which isn't registered yet
        """
        invalid_data = {
            'email': 'efg@test.com',
            'password': 'qwertyQ123'
        }
        partner = PartnerFactory(slug='give2asia')
        response = self.client.post(
            self.partner_login_end_point,
            data=invalid_data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_with_username_not_affiliated_with_partner(self):
        """
        Providing username which isn't affiliated to any partner
        """
        invalid_data = {
            'email': self.user.email,
            'password': self.user.password
        }
        partner = PartnerFactory(slug='give2asia')
        response = self.client.post(
            self.partner_login_end_point,
            data=invalid_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_username_with_nonexistant_partner(self):
        """
        The url does not exist
        """
        invalid_data = {
            'email': 'none@none.com',
            'password': 'none'
        }
        response = self.client.post(
            self.partner_login_end_point,
            data=invalid_data
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_login_with_affiliated_partner_but_non_existing_directory(self):
        """
        The directory of partner does not exist at
        openedx/features/partners/
        """
        valid_data = {
            'email': self.user.email,
            'password': self.user.password
        }
        partner = PartnerFactory(slug='invalid_slug')

        PartnerUserFactory(user_id=self.user.id, partner_id=partner.id)

        response = self.client.post(
            reverse('partner_login', args=['invalid_slug']),
            data=valid_data
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
