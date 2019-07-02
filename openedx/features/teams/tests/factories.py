import factory
from factory.django import DjangoModelFactory

from lms.djangoapps.teams.tests.factories import CourseTeamFactory as BaseCourseTeamFactory
from nodebb.models import TeamGroupChat


TEAM_LANGUAGE = 'en'
TEAM_COUNTRY = 'US'


class CourseTeamFactory(BaseCourseTeamFactory):
    country = TEAM_COUNTRY
    language = TEAM_LANGUAGE

    @factory.post_generation
    def team_group_chat(self, create, expected, **kwargs):
        if create:
            self.save()
            return TeamGroupChatFactory.create(team=self, room_id=0, **kwargs)
        else:
            return None


class TeamGroupChatFactory(DjangoModelFactory):
    class Meta(object):
        model = TeamGroupChat
        django_get_or_create = ('slug',)

    slug = factory.Sequence('TeamGroupChat{0}'.format)
