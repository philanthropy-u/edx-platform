from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from openedx.features.partners.tests.factories import PartnerUserFactory, PartnerFactory
from student.tests.factories import UserFactory


class ResetPasswordTestCases(APITestCase):

    def setUp(self):
        self.partner_login_end_point = reverse('partner_login', args=['give2asia'])
        self.user = UserFactory(username='testuser', password='Abc12345',email='abc@test.com')

    def test_login_with_correct_credentials(self):
        """
                Testing login with valid credentials, i.e, The email is registered and correct password is provided
        """
        valid_data = {
            'email': 'abc@test.com',
            'password': 'Abc12345'
        }

        partner_1 = PartnerFactory(slug='give2asia')

        PartnerUserFactory(user_id=self.user.id, partner_id=partner_1.id)

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
            'email': 'abc@test.com',
            'password': 'incorrectpassword'
        }
        partner_1 = PartnerFactory(slug='give2asia')

        PartnerUserFactory(user_id=self.user.id, partner_id=partner_1.id)

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
        partner_1 = PartnerFactory(slug='give2asia')
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
            'email': 'abc@test.com',
            'password': 'Abc12345'
        }
        partner_1 = PartnerFactory(slug='give2asia')
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
            'email': 'abc@test.com',
            'password': 'Abc12345'
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
            'email': 'abc@test.com',
            'password': 'Abc12345'
        }
        partner_1 = PartnerFactory(slug='slug')

        PartnerUserFactory(user_id=self.user.id, partner_id=partner_1.id)

        response = self.client.post(
            reverse('partner_login', args=['slug']),
            data=valid_data
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
