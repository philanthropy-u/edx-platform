"""
Factories used for smart_referral app tests
"""
import factory

from lms.djangoapps.onboarding.tests.factories import UserFactory
from openedx.features.smart_referral.models import SmartReferral


class SmartReferralFactory(factory.django.DjangoModelFactory):
    """
    Factory for SmartReferral model. It contains fake data and sub-factory for mandatory fields
    """

    class Meta(object):
        model = SmartReferral
        django_get_or_create = ['contact_email', 'user']

    user = factory.SubFactory(UserFactory)
    contact_email = factory.Faker('email')
