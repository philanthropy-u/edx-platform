import factory
from factory.django import DjangoModelFactory
from faker.providers import internet
from openedx.features.partners.models import Partner, PartnerUser, PartnerCommunity
from student.tests.factories import UserFactory

factory.Faker.add_provider(internet)

class PartnerFactory(DjangoModelFactory):
    class Meta(object):
        model = Partner

    label = factory.Faker('name')
    slug = factory.Faker('slug')
    main_logo = 'dummy'
    small_logo = 'dummy'

class PartnerUserFactory(DjangoModelFactory):
    class Meta(object):
        model = PartnerUser

    partner = factory.SubFactory(PartnerFactory)
    user =factory.SubFactory(UserFactory)
