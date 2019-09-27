from django.contrib.auth.models import User
from django.db import models

from common.djangoapps.nodebb.helpers import get_course_id_by_community_id
from nodebb.models import TeamGroupChat
from openedx.core.djangoapps.xmodule_django.models import CourseKeyField

from .constants import CONVERSATIONALIST, TEAM_PLAYER


class Badge(models.Model):
    BADGE_TYPES = (
        CONVERSATIONALIST,
        TEAM_PLAYER
    )

    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    threshold = models.IntegerField(blank=False, null=False)
    type = models.CharField(max_length=100, blank=False, null=False, choices=BADGE_TYPES)
    image = models.CharField(max_length=255, blank=False, null=False)
    date_created = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    @classmethod
    def get_remaining_badges(cls, user_id, community_id, community_type):
        # course_id = get_course_id_by_community_id(community_id)

        badges_in_community = UserBadge.objects.filter(user_id=user_id, 
                                                       community_id=community_id,
                                                       badge_id__type=community_type)

        if badges_in_community:
            latest_earned = badges_in_community.latest('date_earned')
            latest_threshold = Badge.objects.get(pk=latest_earned.badge_id, type=community_type).threshold
            remaining_badges = Badge.objects.filter(type=community_type) \
                                            .exclude(threshold__lte=latest_threshold) \
                                            .order_by('threshold')
            return remaining_badges

        remaining_badges = Badge.objects.filter(type=community_type).order_by('threshold')
        return remaining_badges


class UserBadge(models.Model):
    """
        This model represents what badges are assigned to which users in
        communities (both course and team communities)

        Each object of this model represents the assignment of one badge (specified
        by the `badge_id` foreign key) to a certain user (specified by the `user`
        foreign key) in a `community`. Each `community` is related to a course
        which is specified by the `course_id`. A certain badge is only awarded once
        in a community, the unique_together constraint in Meta class makes sure
        that there are no duplicate objects in the model.
    """
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    course_id = CourseKeyField(max_length=255, db_index=True, db_column='course_id', null=False)
    community_id = models.IntegerField(blank=False, null=False, db_column='community_id')
    date_earned = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'badge', 'course_id', 'community_id')

    def __unicode__(self):
        return 'User: ' + str(self.user.id) + ', Badge: ' + str(self.badge.id)

    @classmethod
    def assign_badge(cls, user_id, badge_id, community_id):
        course_id = get_course_id_by_community_id(community_id)
        
        try:
            badge_type = Badge.objects.get(id=badge_id).type
        except:
            raise Exception('There exists no badge with id %d' % int(badge_id))

        if course_id is CourseKeyField.Empty:
            try:
                team_room_id = TeamGroupChat.objects.get(room_id=community_id)
            except:
                raise Exception('No discussion community or team with id %d' % int(community_id))

        if course_id is CourseKeyField.Empty and badge_type == CONVERSATIONALIST[0] or \
           course_id is not CourseKeyField.Empty and badge_type == TEAM_PLAYER[0]:
            raise Exception('Badge %d is a %s badge, wrong community' % (int(badge_id), badge_type))

        obj, created = UserBadge.objects.get_or_create(
            user_id=user_id,
            badge_id=badge_id,
            course_id=course_id,
            community_id=community_id
        )
