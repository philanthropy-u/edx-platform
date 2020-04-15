import factory

from openedx.features.job_board.models import Job


class JobFactory(factory.django.DjangoModelFactory):
    """Factory for idea model. It contains fake data or sub-factories for all mandatory fields"""

    class Meta(object):
        model = Job

    title = factory.Faker('pystr', min_chars=1, max_chars=255)
    company = factory.Faker('pystr', min_chars=1, max_chars=255)
    type = 'remote'
    compensation = 'volunteer'
    hours = 'fulltime'
    city = 'Lahore'
    country = 'PK'
    description = factory.Faker('pystr', min_chars=1, max_chars=255)
    contact_email = factory.Faker('email')

