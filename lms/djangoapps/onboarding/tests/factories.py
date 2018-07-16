import factory
from factory.django import DjangoModelFactory

from lms.djangoapps.onboarding.models import EnglishProficiency, EducationLevel, RoleInsideOrg, OrgSector, \
    OperationLevel, FocusArea, TotalEmployee


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


class RoleInsideOrgFactory(DjangoModelFactory):
    class Meta(object):
        model = RoleInsideOrg

    order = factory.Sequence(u'{0}'.format)
    code = ""
    label = ""


class OrgSectorFactory(DjangoModelFactory):
    class Meta(object):
        model = OrgSector

    order = factory.Sequence(u'{0}'.format)
    code = ""
    label = ""


class OperationLevelFactory(DjangoModelFactory):
    class Meta(object):
        model = OperationLevel

    order = factory.Sequence(u'{0}'.format)
    code = ""
    label = ""


class FocusAreaFactory(DjangoModelFactory):
    class Meta(object):
        model = FocusArea

    order = factory.Sequence(u'{0}'.format)
    code = ""
    label = ""


class TotalEmployeeFactory(DjangoModelFactory):
    class Meta(object):
        model = TotalEmployee

    order = factory.Sequence(u'{0}'.format)
    code = ""
    label = ""
