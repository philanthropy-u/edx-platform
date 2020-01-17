from factory.django import DjangoModelFactory

from openedx.features.partners.models import Partner, PartnerUser
from lms.djangoapps.onboarding.models import Organization


class PartnerFactory(DjangoModelFactory):
    """ Partner factory."""
    class Meta:
        model = Partner


class PartnerUserFactory(DjangoModelFactory):
    """ Partner user factory."""
    class Meta:
        model = PartnerUser


class OrganizationFactory(DjangoModelFactory):
    """ Organization creation factory."""

    class Meta(object):
        model = Organization
