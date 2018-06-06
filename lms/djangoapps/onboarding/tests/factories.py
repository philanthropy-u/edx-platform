import factory
from factory.django import DjangoModelFactory

from lms.djangoapps.onboarding.models import EnglishProficiency, EducationLevel


class EnglishProficiencyFactory(DjangoModelFactory):
    class Meta(object):
        model = EnglishProficiency

    order = factory.Sequence(u'{0}'.format)
    code = ""
    label = ""


class EducationLevelFactory(DjangoModelFactory):
    class Meta(object):
        model = EducationLevel

    order = factory.Sequence(u'{0}'.format)
    code = ""
    label = ""
