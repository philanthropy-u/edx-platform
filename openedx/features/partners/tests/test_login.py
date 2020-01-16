from django.contrib.auth.models import User


from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from openedx.features.partners.tests.factories import PartnerUserFactory, PartnerFactory

from student.tests.factories import UserFactory

class ResetPasswordTestCases(APITestCase):
    def setUp(self):
        self.end_point = reverse('partner_login',args=['give2asia'])

    def test_login_with_correct_credntials(self):
        self.valid_data = {
            'email': 'abc@test.com',
            'password': 'Abc12345'
        }
        self.partner = User.objects.create_user(username='testuser', password='Abc12345',email='abc@test.com')
        partner_1 = PartnerFactory(label="partner_1", main_logo='abc', small_logo='xyz', slug='give2asia')

        PartnerUserFactory(user_id=self.partner.id, partner_id=partner_1.id)

        response = self.client.post(
            self.end_point,
            data=self.valid_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_login_with_incorrect_password(self):
        self.invalid_data = {
            'email': 'abc@test.com',
            'password': 'incorrectpassword'
        }
        self.partner = User.objects.create_user(username='testuser', password='Abc12345',email='abc@test.com')
        partner_1 = PartnerFactory(label="partner_1", main_logo='abc', small_logo='xyz', slug='give2asia')

        PartnerUserFactory(user_id=self.partner.id, partner_id=partner_1.id)

        response = self.client.post(
            self.end_point,
            data=self.invalid_data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_with_not_registered_username(self):
        self.invalid_data = {
            'email': 'abc@test.com',
            'password': 'qwertyQ123'
        }
        partner_1 = PartnerFactory(label="partner_1", main_logo='abc', small_logo='xyz', slug='give2asia')
        response = self.client.post(
            self.end_point,
            data=self.invalid_data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_login_with_username_not_affiliated_with_partner(self):
        self.invalid_data = {
            'email': 'abc@test.com',
            'password': 'Abc12345'
        }
        self.partner = User.objects.create_user(username='testuser', password='Abc12345',email='abc@test.com')
        partner_1 = PartnerFactory(label="partner_1", main_logo='abc', small_logo='xyz', slug='give2asia')
        response = self.client.post(
            self.end_point,
            data=self.invalid_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_username_with_nonexistant_partner(self):
        self.invalid_data = {
            'email': 'abc@test.com',
            'password': 'Abc12345'
        }
        self.partner = User.objects.create_user(username='testuser', password='Abc12345',email='abc@test.com')
        response = self.client.post(
            self.end_point,
            data=self.invalid_data
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_login_with_affiliated_partner_but_non_existing_directory(self):
        self.valid_data = {
            'email': 'abc@test.com',
            'password': 'Abc12345'
        }
        self.partner = User.objects.create_user(username='testuser', password='Abc12345', email='abc@test.com')
        partner_1 = PartnerFactory(label="partner_1", main_logo='abc', small_logo='xyz', slug='slug')

        PartnerUserFactory(user_id=self.partner.id, partner_id=partner_1.id)

        response = self.client.post(
            reverse('partner_login',args=['slug']),
            data=self.valid_data
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
