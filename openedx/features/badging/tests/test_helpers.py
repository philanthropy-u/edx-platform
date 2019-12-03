import factory
import mock

from django.db.models import signals

from lms.djangoapps.teams.tests.factories import CourseTeamFactory, CourseTeamMembershipFactory
from nodebb.constants import (
    TEAM_PLAYER_ENTRY_INDEX,
    CONVERSATIONALIST_ENTRY_INDEX
)
from openedx.features.badging.constants import CONVERSATIONALIST, TEAM_PLAYER
from openedx.features.teams.tests.factories import TeamGroupChatFactory
from student.tests.factories import CourseEnrollmentFactory
from student.tests.factories import UserFactory
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory

from .factories import BadgeFactory, UserBadgeFactory
from .. import helpers as badge_helpers
from ..models import Badge


class BadgeHelperTestCases(ModuleStoreTestCase):

    def setUp(self):
        super(BadgeHelperTestCases, self).setUp()
        self.user = UserFactory()
        self.course1 = CourseFactory(org="test1", number="123", run="1", display_name="ABC")
        self.type_conversationalist = CONVERSATIONALIST[CONVERSATIONALIST_ENTRY_INDEX] # badge type


    def test_populate_trophycase_with_empty_course_list(self):
        trophycase_dict = badge_helpers.populate_trophycase(user=self.user, courses=list(), earned_badges=mock.ANY)
        self.assertEqual(trophycase_dict, dict())

    def test_populate_trophycase_with_courses_none(self):
        with self.assertRaises(TypeError):
            badge_helpers.populate_trophycase(user=self.user, courses=None, earned_badges=mock.ANY)

    @mock.patch('openedx.features.badging.helpers.get_course_badges')
    def test_populate_trophycase_successful_and_ordered_by_course_name(self, mock_get_course_badges):
        mock_get_course_badges.return_value = {"badges": 'mocked badges'}

        course2 = CourseFactory(org="test2", number="123", run="1", display_name="XYZ")
        course3 = CourseFactory(org="test3", number="123", run="1", display_name="Course3")
        CourseFactory(org="test4", number="123", run="1", display_name="Course4")

        # Enroll in three courses, two active and one inactive
        CourseEnrollmentFactory(user=self.user, course_id=self.course1.id, is_active=True)
        CourseEnrollmentFactory(user=self.user, course_id=course2.id, is_active=True)
        CourseEnrollmentFactory(user=self.user, course_id=course3.id, is_active=False)

        courses = [
            (self.course1.id, self.course1.display_name),
            (course2.id, course2.display_name)
        ]
        trophycase_dict = badge_helpers.populate_trophycase(self.user, courses, earned_badges=mock.ANY)

        expected_return_value = dict([
            (u'test1/123/1', {'display_name': u'ABC', 'badges': 'mocked badges'}),
            (u'test2/123/1', {'display_name': u'XYZ', 'badges': 'mocked badges'})
        ])

        self.assertEqual(expected_return_value, trophycase_dict)

        # assert order of courses by display name
        course_detail = trophycase_dict.values()
        self.assertEqual(expected_return_value['test1/123/1'], course_detail[0])
        self.assertEqual(expected_return_value['test2/123/1'], course_detail[1])

    @mock.patch('openedx.features.badging.helpers.Badge.objects.all')
    def test_course_badges_with_empty_badge_queryset(self, mock_badge_objects_all):
        message = 'Raising fake exception, if badge_queryset is none'
        mock_badge_objects_all.side_effect = Exception(message)

        with self.assertRaises(Exception) as error:
            badge_helpers.get_course_badges(user=self.user, course_id=mock.ANY, earned_badges=mock.ANY,
                                            badge_queryset=Badge.objects.none())

        self.assertEqual(str(error.exception), message)

    @mock.patch('openedx.features.badging.helpers.add_badge_earned_date')
    @mock.patch('openedx.features.badging.helpers.filter_earned_badge_by_joined_team')
    @mock.patch('openedx.features.badging.helpers.is_teams_feature_enabled')
    @mock.patch('openedx.features.badging.helpers.get_course_by_id')
    def test_course_badges_successfully(self, mock_get_course_by_id,
                                        mock_is_teams_feature_enabled,
                                        mock_filter_earned_badge_by_joined_team,
                                        mock_add_badge_earned_date):
        mock_get_course_by_id.return_value = mock.ANY
        mock_is_teams_feature_enabled.return_value = False
        mock_filter_earned_badge_by_joined_team.return_value = False, list()

        badge1 = BadgeFactory(type=TEAM_PLAYER[TEAM_PLAYER_ENTRY_INDEX], threshold=2)
        badge2 = BadgeFactory(type=self.type_conversationalist, threshold=2)
        badge3 = BadgeFactory(type=self.type_conversationalist, threshold=5)

        badges = badge_helpers.get_course_badges(self.user, self.course1.id, earned_badges=mock.ANY)

        expected_result = {
            'badges': {
                'conversationalist': [{
                    'description': None, 'image': badge2.image, 'threshold': 2L,
                    'date_created': badge2.date_created, 'type': u'conversationalist',
                    u'id': badge2.id, 'name': badge2.name
                }, {
                    'description': None, 'image': badge3.image, 'threshold': 5L,
                    'date_created': badge3.date_created, 'type': u'conversationalist',
                    u'id': badge3.id, 'name': badge3.name
                }]
            }
        }

        self.assertEqual(expected_result, badges)

        expected_conversationalist_badges = expected_result['badges']['conversationalist']
        self.assertEqual(expected_conversationalist_badges[0]['threshold'], badge2.threshold)
        self.assertEqual(expected_conversationalist_badges[1]['threshold'], badge3.threshold)

        badge_keys = badges['badges'].keys()
        self.assertIn('conversationalist', badge_keys)
        self.assertNotIn('team', badge_keys)

    @mock.patch('openedx.features.badging.helpers.add_badge_earned_date')
    @mock.patch('openedx.features.badging.helpers.filter_earned_badge_by_joined_team')
    @mock.patch('openedx.features.badging.helpers.is_teams_feature_enabled')
    @mock.patch('openedx.features.badging.helpers.get_course_by_id')
    def test_course_badges_user_not_joined_any_course_team(self, mock_get_course_by_id,
                                                           mock_is_teams_feature_enabled,
                                                           mock_filter_earned_badge_by_joined_team,
                                                           mock_add_badge_earned_date):
        mock_get_course_by_id.return_value = mock.ANY
        mock_is_teams_feature_enabled.return_value = True
        mock_filter_earned_badge_by_joined_team.return_value = False, list()

        badge = BadgeFactory(type=self.type_conversationalist, threshold=2)

        badges = badge_helpers.get_course_badges(self.user, self.course1.id, earned_badges=mock.ANY)

        expected_result = {
            'badges': {
                'conversationalist': [{
                    'description': None, 'image': badge.image, 'threshold': 2L,
                    'date_created': badge.date_created, 'type': u'conversationalist',
                    u'id': badge.id, 'name': badge.name
                }],
                'team': []
            },
            'team_joined': False
        }

        self.assertEqual(expected_result, badges)

    def test_badge_earned_date_no_course_badges(self):
        with self.assertRaises(TypeError):
            badge_helpers.add_badge_earned_date(self.course1.id, course_badges=None, earned_badges=mock.ANY)

    def test_badge_earned_date_no_earned_badges(self):
        badge = BadgeFactory(type=self.type_conversationalist, threshold=2)
        course_badges = [badge, ]
        with self.assertRaises(TypeError):
            badge_helpers.add_badge_earned_date(self.course1.id, course_badges, earned_badges=None)

    def test_badge_earned_date_course_badges_subset_of_earned_badges(self):
        course2 = CourseFactory(org="test2", number="123", run="1", display_name="XYZ")

        badge1 = BadgeFactory(type=self.type_conversationalist, threshold=2)
        badge2 = BadgeFactory(type=self.type_conversationalist, threshold=5)

        user_badge_1 = UserBadgeFactory(user=self.user, course_id=self.course1.id, badge=badge1)
        user_badge_2 = UserBadgeFactory(user=self.user, course_id=course2.id, badge=badge2)

        course_badges = list(
            Badge.objects.all().values()
        )
        earned_badges = [user_badge_1, user_badge_2]
        badge_helpers.add_badge_earned_date(self.course1.id, course_badges, earned_badges)

        # get badges by index, since list maintains insertion order
        self.assertIsNotNone(course_badges[0]['date_earned'])
        self.assertRaises(KeyError, lambda: course_badges[1]['date_earned'])

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def test_filter_earned_badge_by_joined_team(self):
        badge1 = BadgeFactory(type=self.type_conversationalist, threshold=2)
        badge2 = BadgeFactory(type=self.type_conversationalist, threshold=2)
        user_badge1 = UserBadgeFactory(user=self.user, course_id=self.course1.id, badge=badge1, community_id=100)
        user_badge2 = UserBadgeFactory(user=self.user, course_id=self.course1.id, badge=badge2, community_id=101)

        earned_badges = [user_badge1, user_badge2]

        course_team_from_factory = CourseTeamFactory(course_id=self.course1.id, team_id='team1')
        CourseTeamMembershipFactory(user=self.user, team=course_team_from_factory)
        TeamGroupChatFactory(team=course_team_from_factory, room_id=100)

        course_team, earned_badges = badge_helpers.filter_earned_badge_by_joined_team(
            self.user, self.course1, earned_badges)

        self.assertIsNotNone(course_team)
        self.assertEqual(earned_badges, [user_badge1])

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def test_filter_earned_badge_by_joined_team_invalid_room_id(self):
        course_team_from_factory = CourseTeamFactory(course_id=self.course1.id, team_id='team1')
        CourseTeamMembershipFactory(user=self.user, team=course_team_from_factory)

        with self.assertRaises(Exception):
            badge_helpers.filter_earned_badge_by_joined_team(self.user, self.course1, earned_badges=mock.ANY)

    def test_filter_earned_badge_by_joined_team_course_with_no_team(self):
        course_team, earned_badges = badge_helpers.filter_earned_badge_by_joined_team(
            self.user, self.course1, earned_badges=mock.ANY)

        self.assertIsNone(course_team)
        self.assertEqual(earned_badges, list())
