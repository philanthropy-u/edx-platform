import factory

from django.db.models import signals
from django.test import TestCase
from mock import patch

from lms.djangoapps.teams.tests.factories import CourseTeamFactory, CourseTeamMembershipFactory
from nodebb.constants import TEAM_PLAYER_ENTRY_INDEX
from opaque_keys.edx.keys import CourseKey
from openedx.features.badging.constants import BADGE_ID_KEY, TEAM_PLAYER
from openedx.features.badging.models import UserBadge
from openedx.features.teams.tests.factories import TeamGroupChatFactory
from student.tests.factories import UserFactory

from .factories import BadgeFactory, UserBadgeFactory


class MissingBadgeTestCase(TestCase):

    def setUp(self):
        self.type_team = TEAM_PLAYER[TEAM_PLAYER_ENTRY_INDEX]
        self.team_badge = BadgeFactory(type=self.type_team)
        self.course_key = CourseKey.from_string('abc/course/123')

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def test_assign_missing_team_badges(self):
        user = UserFactory()
        user2 = UserFactory()
        course_team = CourseTeamFactory(course_id=self.course_key, team_id='team1')
        team_group_chat = TeamGroupChatFactory(team=course_team, room_id=200)

        # Add first user to team in course
        CourseTeamMembershipFactory(user=user, team=course_team)

        # Assigning badge to user in team
        UserBadgeFactory(user=user, badge=self.team_badge, community_id=team_group_chat.room_id)

        assigned_user_badges = UserBadge.objects.filter(
            user_id=user.id
        ).values(BADGE_ID_KEY)

        # Add second user to team in course
        CourseTeamMembershipFactory(user=user2, team=course_team)

        # Assigning missing badges to second user
        UserBadge.assign_missing_team_badges(user2.id, course_team.id)

        assigned_user2_badges = UserBadge.objects.filter(
            user_id=user2.id
        ).values(BADGE_ID_KEY)

        self.assertEqual(len(assigned_user_badges), len(assigned_user2_badges))

    def test_assign_missing_team_badges_with_invalid_params(self):
        with self.assertRaises(Exception):
            UserBadge.assign_missing_team_badges(None, None)

    @patch('openedx.features.badging.models.UserBadge.objects.get_or_create')
    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def test_assign_missing_team_badges_distinct_earned_badges(self, mock_get_or_create):
        user = UserFactory()
        user2 = UserFactory()
        user3 = UserFactory()
        course_team = CourseTeamFactory(course_id=self.course_key, team_id='team1')
        team_group_chat = TeamGroupChatFactory(team=course_team, room_id=200)

        # Add two users to team in course
        CourseTeamMembershipFactory(user=user, team=course_team)
        CourseTeamMembershipFactory(user=user2, team=course_team)

        # Assigning badge to users in team
        UserBadgeFactory(user=user, badge=self.team_badge, community_id=team_group_chat.room_id)
        UserBadgeFactory(user=user2, badge=self.team_badge, community_id=team_group_chat.room_id)

        # Adding third user to team in course
        CourseTeamMembershipFactory(user=user3, team=course_team)

        # Assigning missing badges to third user
        UserBadge.assign_missing_team_badges(user3.id, course_team.id)

        # The mocked function should only be called once
        self.assertEqual(mock_get_or_create.call_count, 1)
