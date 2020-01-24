import factory
from factory.django import DjangoModelFactory

from custom_settings.models import CustomSettings

from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from openedx.features.course_card.models import CourseCard
from openedx.features.partners.models import Partner, PartnerUser, PartnerCommunity
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

    class Meta:
        model = Organization


class CustomSettingsFactory(DjangoModelFactory):
    """ Partner CustomSettings Factory """

    class Meta:
        model = CustomSettings


class CourseOverviewFactory(DjangoModelFactory):
    """ Course overview factory """

    class Meta(object):
        model = CourseOverview

    version = CourseOverview.VERSION
    org = 'edX'

    display_name = factory.Faker('word')
    # enrollment start date is less than current date
    enrollment_start = factory.Faker('date_time_between', start_date='-10d', end_date='now')
    # enrollment end date greater than current date
    enrollment_end = factory.Faker('date_time_between', start_date='+1d', end_date='+10d')


class CourseCardFactory(DjangoModelFactory):
    """ Course card factory """

    class Meta:
        model = CourseCard

    is_enabled = True


class PartnerCommunityFactory(DjangoModelFactory):
    """ Partner Community factory. """

    class Meta:
        model = PartnerCommunity

    community_id = factory.Sequence(lambda n: n)

