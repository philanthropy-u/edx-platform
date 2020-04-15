import factory
from factory import fuzzy

from openedx.features.job_board.constants import JOB_COMPENSATION_CHOICES, JOB_HOURS_CHOICES, JOB_TYPE_CHOICES
from openedx.features.job_board.models import Job


class JobFactory(factory.django.DjangoModelFactory):

    class Meta():
        model = Job

    title = factory.Faker('pystr', min_chars=1, max_chars=255)
    company = factory.Faker('pystr', min_chars=1, max_chars=255)
    type = fuzzy.FuzzyChoice(JOB_TYPE_CHOICES)
    compensation = fuzzy.FuzzyChoice(JOB_COMPENSATION_CHOICES)
    hours = fuzzy.FuzzyChoice(JOB_HOURS_CHOICES)
    city = 'Lahore'
    country = 'PK'
    description = factory.Faker('pystr', min_chars=1, max_chars=255)
    contact_email = factory.Faker('email')

