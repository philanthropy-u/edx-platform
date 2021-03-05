"""
    Models related to nodeBB integrations
"""
from django.db import models
from model_utils.models import TimeStampedModel

from lms.djangoapps.teams.models import CourseTeam
from openedx.core.djangoapps.xmodule_django.models import CourseKeyField


class DiscussionCommunity(TimeStampedModel):
    """
        Model to store each course related communities
    """

    course_id = CourseKeyField(max_length=255, db_index=True)
    community_url = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return "%s" % self.community_url

    def __unicode__(self):
        return u'DiscussionCommunity: course_id: {}, community_url: {}'.format(self.course_id, self.community_url)


class TeamGroupChat(TimeStampedModel):
    """
        Model to store team related group chats/discussion categories
    """

    team = models.ForeignKey(CourseTeam, related_name='team')
    room_id = models.IntegerField()
    slug = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return "%s" % self.room_id

    def __unicode__(self):
        return u'TeamGroupChat: team: {}, room_id: {}, slug: {}'.format(self.team, self.room_id, self.slug)
