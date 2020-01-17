from ddt import ddt, data

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from openedx.features.partners.tests.factories import PartnerFactory, OrganizationFactory
from openedx.core.lib.api.test_utils import ApiTestCase
from lms.djangoapps.onboarding.models import Organization


@ddt
class RegistrationViewTest(ApiTestCase):
    """Tests for the registration"""

    NAME = "bob james"
    COUNTRY = "Pakistan"
    ORGANIZATION = "arbisoft"
    EMAIL = "bob@example.com"
    USERNAME = "bob"
    PASSWORD = "Test@12345"
    TERMS_OF_SERVICE = True

    def setUp(self):
        super(RegistrationViewTest, self).setUp()
        self.organization = OrganizationFactory(
            label='arbisoft'
        )
        self.partner = PartnerFactory.create(slug="give2asia", label="arbisoft")
        self.url = reverse("partner_register", args=["give2asia"])

    def test_put_not_allowed(self):
        response = self.client.put(self.url)
        self.assertHttpMethodNotAllowed(response)

    def test_delete_not_allowed(self):
        response = self.client.delete(self.url)
        self.assertHttpMethodNotAllowed(response)

    def test_register(self):
        # Create a new partner user
        response = self.client.post(self.url, {
            "name": self.NAME,
            "organization_name": self.organization.label,
            "country": self.COUNTRY,
            "email": self.EMAIL,
            "username": self.USERNAME,
            "password": self.PASSWORD,
            'terms_of_service': self.TERMS_OF_SERVICE
        })
        self.assertHttpOK(response)
        user = User.objects.get(username=self.USERNAME)
        organization = Organization.objects.filter(label__iexact=self.organization.label).first()

        self.assertEqual(self.USERNAME, user.username)
        self.assertEqual(self.EMAIL, user.email)
        self.assertEqual(self.NAME.split(" ", 1)[0], user.first_name)
        self.assertEqual(self.NAME.split(" ", 1)[1], user.last_name)
        self.assertEqual(True, user.is_active)
        self.assertEqual(self.organization.label, organization.label)
        self.assertHttpOK(response)


    @data(
        {"name": ""},
        {"country": ""},
        {"email": ""},
        {"username": ""},
        {"password": "invalid"},
        {"terms_of_service": ""}
    )
    def test_register_invalid_input(self, invalid_fields):
        # Initially, the field values are all valid
        data = {
            "name": self.NAME,
            "organization_name": self.organization.label,
            "country": self.COUNTRY,
            "email": self.EMAIL,
            "username": self.USERNAME,
            "password": self.PASSWORD,
            'terms_of_service': self.TERMS_OF_SERVICE
        }
        # Override the valid fields, making the input invalid
        data.update(invalid_fields)

        # Attempt to create the partner user, expecting an error response
        response = self.client.post(self.url, data)
        self.assertHttpBadRequest(response)

    @data("username", "country", "password", "email", "terms_of_service")
    def test_register_missing_required_field(self, missing_field):
        data = {
            "username": self.USERNAME,
            "password": self.PASSWORD,
            "email": self.EMAIL,
            "name": self.NAME,
            "country": self.COUNTRY,
            "organization_name": self.organization.label,
            'terms_of_service': self.TERMS_OF_SERVICE
        }

        # delete required field
        if missing_field in data:
            del data[missing_field]

        # Send a request with missing field
        response = self.client.post(self.url, data)
        self.assertHttpBadRequest(response)
