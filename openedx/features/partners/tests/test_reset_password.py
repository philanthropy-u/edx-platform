from django.contrib.auth.models import User
from django.urls import reverse
from openedx.features.partners.tests.factories import PartnerUserFactory, PartnerFactory
from rest_framework.test import APITestCase
from rest_framework import status
from student.tests.factories import UserFactory


class ResetPasswordTestCases(APITestCase):

    def setUp(self):
        self.end_point = reverse('partner_reset_password')

    def test_valid_partner_email(self):
        valid_data = {
            'email': 'abc@test.com'
        }
        user = UserFactory(username='testuser', password='12345',email='abc@test.com')
        partner_1 = PartnerFactory(label="partner_1", main_logo='abc', small_logo='xyz', slug='partner_1')

        PartnerUserFactory(user_id=user.id, partner_id=partner_1.id)

        response = self.client.post(
            self.end_point,
            data=valid_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_partner_email_not_affiliated_to_partner(self):
        valid_data = {
            'email': 'abc@test.com'
        }
        user = UserFactory(username='testuser', password='12345',email='abc@test.com')

        response = self.client.post(
            self.end_point,
            data=valid_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_partner_email(self):
        invalid_data = {
            'email': 'efg@test.com'
        }
        response = self.client.post(
            self.end_point,
            data=invalid_data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


