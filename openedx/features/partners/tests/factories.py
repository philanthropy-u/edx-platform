from factory.django import DjangoModelFactory

from openedx.features.partners.models import Partner, PartnerUser, PartnerCommunity


class PartnerFactory(DjangoModelFactory):
    class Meta(object):
        model = Partner

    label = 'temp'
    main_logo = 'dummy'
    small_logo = 'dummy'
class PartnerUserFactory(DjangoModelFactory):
    class Meta(object):
        model = PartnerUser
