import factory

from django.db.models import signals
from django.test import TestCase

from lms.djangoapps.teams.tests.factories import CourseTeamFactory, CourseTeamMembershipFactory
from nodebb.constants import TEAM_PLAYER_ENTRY_INDEX
from opaque_keys.edx.keys import CourseKey
from openedx.features.badging.constants import BADGE_ID_KEY, TEAM_BADGE_ERROR, TEAM_PLAYER
from openedx.features.badging.models import UserBadge
from openedx.features.teams.tests.factories import TeamGroupChatFactory
from student.tests.factories import UserFactory
from .factories import BadgeFactory


class MissingBadgeTestCase(TestCase):

    def setUp(self):
        self.type_team = TEAM_PLAYER[TEAM_PLAYER_ENTRY_INDEX]
        self.team_badges = [BadgeFactory(type=self.type_team),
                            BadgeFactory(type=self.type_team),
                            BadgeFactory(type=self.type_team),
                            BadgeFactory(type=self.type_team),
                            BadgeFactory(type=self.type_team),
                            BadgeFactory(type=self.type_team)]
        self.course_key = CourseKey.from_string('test/course/123')


    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def test_assign_missing_team_badges(self):
        user = UserFactory(id=1)
        user2 = UserFactory(id=2)
        course_team = CourseTeamFactory(course_id=self.course_key, team_id='team1')
        team_group_chat = TeamGroupChatFactory(team=course_team, room_id=200)

        # Add first user to team in course
        CourseTeamMembershipFactory(user=user, team=course_team)

        #Assigning 3 badges to user in team
        UserBadge.assign_badge(user_id=user.id, badge_id=self.team_badges[0].id, community_id=team_group_chat.room_id)
        UserBadge.assign_badge(user_id=user.id, badge_id=self.team_badges[1].id, community_id=team_group_chat.room_id)
        UserBadge.assign_badge(user_id=user.id, badge_id=self.team_badges[2].id, community_id=team_group_chat.room_id)

        assigned_user_badges = UserBadge.objects.filter(
            user_id=user.id
        ).values(BADGE_ID_KEY)
        assigned_user2_badges = UserBadge.objects.filter(
            user_id=user2.id
        ).values(BADGE_ID_KEY)
        self.assertEqual(len(assigned_user_badges), 3)
        self.assertEqual(len(assigned_user2_badges), 0) #Is not part of team so no badges assigned currently

        # Add second user to team in course
        CourseTeamMembershipFactory(user=user2, team=course_team)

        # Assigning missing badges to second user
        UserBadge.assign_missing_team_badges(user2.id, course_team.id)

        assigned_user2_badges = UserBadge.objects.filter(
            user_id=user2.id
        ).values(BADGE_ID_KEY)

        self.assertEqual(len(assigned_user_badges), len(assigned_user2_badges))
        # Comparing badges of both users
        for count in range(0,len(assigned_user_badges)):
            self.assertEqual(assigned_user_badges[count], assigned_user2_badges[count])

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def test_exception(self):
        exception_raised = False
        try:
            UserBadge.assign_missing_team_badges(None,None)
        except:
            exception_raised = True
        self.assertEqual(True, exception_raised)

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def test_badge_from_other_team_should_not_be_assigned(self):
        user = UserFactory(id=1)
        user2 = UserFactory(id=2)
        user3 = UserFactory(id=3)

        course_team = CourseTeamFactory(course_id=self.course_key, team_id='team1')
        team_group_chat = TeamGroupChatFactory(team=course_team, room_id=200)

        another_course_team = CourseTeamFactory(course_id=self.course_key, team_id='team2')
        another_team_group_chat = TeamGroupChatFactory(team=another_course_team, room_id=900)

        # Add first user to team in course
        CourseTeamMembershipFactory(user=user, team=course_team)

        # Assigning 3 badges to user in team
        UserBadge.assign_badge(user_id=user.id, badge_id=self.team_badges[0].id, community_id=team_group_chat.room_id)
        UserBadge.assign_badge(user_id=user.id, badge_id=self.team_badges[1].id, community_id=team_group_chat.room_id)
        UserBadge.assign_badge(user_id=user.id, badge_id=self.team_badges[2].id, community_id=team_group_chat.room_id)

        # Assigning 4 badges to user3 who happens to be in another team
        UserBadge.assign_badge(user_id=user3.id, badge_id=self.team_badges[0].id,
                               community_id=another_team_group_chat.room_id)
        UserBadge.assign_badge(user_id=user3.id, badge_id=self.team_badges[1].id,
                               community_id=another_team_group_chat.room_id)
        UserBadge.assign_badge(user_id=user3.id, badge_id=self.team_badges[2].id,
                               community_id=another_team_group_chat.room_id)
        UserBadge.assign_badge(user_id=user3.id, badge_id=self.team_badges[3].id,
                               community_id=another_team_group_chat.room_id)

        # Add second user to team in course
        CourseTeamMembershipFactory(user=user2, team=course_team)

        # Assigning missing badges to second user
        UserBadge.assign_missing_team_badges(user2.id, course_team.id)

        assigned_user2_badges = UserBadge.objects.filter(
            user_id=user2.id
        ).values(BADGE_ID_KEY)

        #team_badges[3] is assigned to a user in another team so should not be assigned to user2
        if self.team_badges[3] not in assigned_user2_badges:
            self.assertEqual(True, True)
        else:
            self.assertEqual(True,False)
