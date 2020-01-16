from django.contrib.auth.models import User


from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from openedx.features.partners.tests.factories import PartnerUserFactory, PartnerFactory

from student.tests.factories import UserFactory

class ResetPasswordTestCases(APITestCase):
    def setUp(self):

        self.end_point = reverse('partner_reset_password')

    def test_valid_partner_email_with_authenticated_user(self):
        self.user = UserFactory()
        self.client.force_authenticate(self.user)

        self.valid_data = {
            'email': 'abc@test.com'
        }
        self.partner = User.objects.create_user(username='testuser', password='12345',email='abc@test.com')
        partner_1 = PartnerFactory(label="partner_1", main_logo='abc', small_logo='xyz', slug='partner_1')

        PartnerUserFactory(user_id=self.partner.id, partner_id=partner_1.id)

        response = self.client.post(
            self.end_point,
            data=self.valid_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)




    def test_valid_partner_email_with_unauthenticated_user(self):
        self.valid_data = {
            'email': 'abc@test.com'
        }
        self.partner = User.objects.create_user(username='testuser', password='12345',email='abc@test.com')
        partner_1 = PartnerFactory(label="partner_1", main_logo='abc', small_logo='xyz', slug='partner_1')

        PartnerUserFactory(user_id=self.partner.id, partner_id=partner_1.id)

        response = self.client.post(
            self.end_point,
            data=self.valid_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)






    def test_invalid_partner_email(self):
        self.invalid_data = {
            'email': 'efg@test.com'
        }
        response = self.client.post(
            self.end_point,
            data=self.invalid_data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
