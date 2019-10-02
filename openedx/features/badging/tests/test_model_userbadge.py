from mock import patch

from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from lms.djangoapps.teams.models import CourseTeam
from openedx.core.djangoapps.xmodule_django.models import CourseKeyField

from common.djangoapps.nodebb.constants import (
    COMMUNITY_ID_SPLIT_INDEX,
    TEAM_PLAYER_ENTRY_INDEX,
    CONVERSATIONALIST_ENTRY_INDEX
)

from nodebb.models import TeamGroupChat
from openedx.features.badging.constants import CONVERSATIONALIST, TEAM_PLAYER
from openedx.features.badging.models import Badge, UserBadge


class UserBadgeModelTestCases(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.badge_team = Badge(name="Sample Badge",
                                description="This is a sample badge",
                                threshold=30,
                                type="team",
                                image="path/too/image",
                                date_created=timezone.now())
        self.badge_team.save()

        self.badge_convo = Badge(name="Sample Badge",
                                 description="This is a sample badge",
                                 threshold=30,
                                 type="conversationalist",
                                 image="path/too/image",
                                 date_created=timezone.now())
        self.badge_convo.save()

    def test_save_userbadge_normal(self):
        """
        Trying to save a UserBadge object with expected arguments
        """
        userbadge = UserBadge(user=self.user,
                              badge=self.badge_convo,
                              course_id=CourseKeyField.Empty,
                              community_id=-1,
                              date_earned=timezone.now())

        self.assertEqual(userbadge.save(), None)

    def test_save_duplicate_badge(self):
        """
        Trying to save a duplicate UserBadge object with expected arguments

        Raises IntegrityError upon trying to save the second object with
        the same arguments
        """
        UserBadge.objects.create(user=self.user,
                                 badge=self.badge_convo,
                                 course_id=CourseKeyField.Empty,
                                 community_id=-1,
                                 date_earned=timezone.now())

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                UserBadge.objects.create(user=self.user,
                                         badge=self.badge_convo,
                                         course_id=CourseKeyField.Empty,
                                         community_id=-1,
                                         date_earned=timezone.now())

    def test_course_id_string(self):
        """
        Trying to save UserBadge object with course_id as string
        """
        self.assertTrue(UserBadge.objects.create(user=self.user,
                                                 badge=self.badge_convo,
                                                 course_id="",
                                                 community_id=-1,
                                                 date_earned=timezone.now()))

    def test_community_id_None(self):
        """
        Trying to save UserBadge object with community_id as None
        """
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                UserBadge.objects.create(user=self.user,
                                         badge=self.badge_convo,
                                         course_id="",
                                         community_id=None,
                                         date_earned=timezone.now())

    def test_date_blank_sets_current_date(self):
        """
        Trying to save a UserBadge object with no date_earned
        automatically sets it to current date.
        """
        UserBadge.objects.create(user=self.user,
                                 badge=self.badge_convo,
                                 course_id=CourseKeyField.Empty,
                                 community_id=-1,
                                 date_earned=None)

        time_at_save = timezone.now().replace(microsecond=0)
        saved_time = UserBadge.objects.get(user=self.user).date_earned.replace(microsecond=0)
        self.assertEquals(time_at_save, saved_time)

    @patch('openedx.features.badging.models.get_course_id_by_community_id')
    def test_assign_badge_wrong_badge_id(self, mock_get_community_id):
        """
        Trying to save a UserBadge object with badge id
        that does not exist
        """
        mock_get_community_id.return_value = CourseKeyField.Empty

        with self.assertRaises(Exception):
            with transaction.atomic():
                UserBadge.assign_badge(self.user.id, -1, "-1")

    @patch('openedx.features.badging.models.get_course_id_by_community_id')
    def test_assign_badge_wrong_type_discussion(self, mock_get_community_id):
        """
        Trying to save a UserBadge object giving a conversationalist
        badge with a team community
        """
        mock_get_community_id.return_value = CourseKeyField.Empty
        with self.assertRaises(Exception):
            with transaction.atomic():
                UserBadge.assign_badge(self.user.id, self.badge_convo.id, "-1")

    @patch('openedx.features.badging.models.get_course_id_by_community_id')
    def test_assign_badge_wrong_type_team(self, mock_get_community_id):
        """
        Trying to save a UserBadge object giving a team
        badge with a conversationalist community
        """
        mock_get_community_id.return_value = "some_course_id"
        with self.assertRaises(Exception):
            with transaction.atomic():
                UserBadge.assign_badge(self.user.id, self.badge_team.id, "-1")

    @patch('openedx.features.badging.models.CourseTeamMembership.objects.filter')
    @patch('openedx.features.badging.models.TeamGroupChat.objects.first')
    @patch('openedx.features.badging.models.TeamGroupChat.objects.exclude')
    @patch('openedx.features.badging.models.TeamGroupChat.objects.filter')
    @patch('openedx.features.badging.models.get_course_id_by_community_id')
    def test_assign_badge_team(self, mock_get_community_id, mock_team_group_filter,
                               mock_team_group_exclude, mock_team_group_first,
                               mock_course_team_filter):
        """
        Trying to save a UserBadge object assigning a team badge
        successfully
        """
        mock_get_community_id.return_value = CourseKeyField.Empty
        UserBadge.assign_badge(user_id=self.user.id,
                               badge_id=self.badge_team.id,
                               community_id=-1)

        assert mock_team_group_filter.called
        assert mock_course_team_filter.called

    @patch('openedx.features.badging.models.UserBadge.objects.get_or_create')
    @patch('openedx.features.badging.models.get_course_id_by_community_id')
    def test_assign_badge_community(self, mock_get_community_id, mock_userbadge_create):
        """
        Trying to save a UserBadge object assigning a conversationalist
        badge successfully
        """
        mock_get_community_id.return_value = "some_course_id"
        UserBadge.assign_badge(user_id=self.user.id,
                               badge_id=self.badge_convo.id,
                               community_id=-1)

        assert mock_userbadge_create.called
