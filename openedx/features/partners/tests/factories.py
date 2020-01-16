from factory.django import DjangoModelFactory

from openedx.features.partners.models import Partner, PartnerUser, PartnerCommunity


class PartnerFactory(DjangoModelFactory):
    class Meta(object):
        model = Partner

class PartnerUserFactory(DjangoModelFactory):
    class Meta(object):
        model = PartnerUser
