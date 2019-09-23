from django.contrib.auth.models import User
from django.db import models, IntegrityError
from common.djangoapps.nodebb.helpers import get_course_id_by_community_id
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

    class Meta:
        unique_together = ('user', 'badge', 'course_id', 'community_id')

    def __unicode__(self):
            return 'User: ' + str(self.user.id) + ', Badge: ' + str(self.badge.id)

    @classmethod
    def assign_badge(cls, user_id, badge_id, community_id):
        course_id = get_course_id_by_community_id(community_id)

        obj, created = UserBadge.objects.get_or_create(
            user_id=user_id,
            badge_id=badge_id,
            course_id=course_id,
            community_id=community_id
        )
