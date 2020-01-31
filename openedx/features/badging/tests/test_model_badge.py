from django.contrib.auth.models import User
from django.test import TestCase

from common.djangoapps.nodebb.constants import (
    TEAM_PLAYER_ENTRY_INDEX,
    CONVERSATIONALIST_ENTRY_INDEX
)

from openedx.features.badging.constants import CONVERSATIONALIST, TEAM_PLAYER
from openedx.features.badging.models import Badge

from openedx.features.badging.tests.factories import BadgeFactory, UserBadgeFactory


def get_expected_badge_data(badge):
    return {
        'name': badge.name,
        'description': badge.description,
        'threshold': badge.threshold,
        'type': badge.type,
        'image': badge.image
    }


class BadgeModelTestCases(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')

    def test_save_badge_normal(self):
        """
        Trying to save a Badge object with all the right arguments.
        """
        badge = Badge(name="Sample Badge",
                      description="This is a sample badge",
                      threshold=30,
                      type=CONVERSATIONALIST[CONVERSATIONALIST_ENTRY_INDEX],
                      image="path/to/image",
                      date_created=None)
        self.assertEqual(badge.save(), None)

    def test_badges_empty(self):
        """
        Test get badges if no badge is created
        """
        expected_result = {}
        returned_result = Badge.get_badges(community_type="no_match_")
        self.assertEqual(expected_result, returned_result)

    def test_all_badges(self):
        """
        Test get badges after creating 2 badges
        """
        badge_1 = BadgeFactory(name="badge_1", threshold=30, type=TEAM_PLAYER[TEAM_PLAYER_ENTRY_INDEX])
        badge_2 = BadgeFactory(name="badge_2", threshold=70, type=TEAM_PLAYER[TEAM_PLAYER_ENTRY_INDEX])
        expected_result = {}
        expected_result["1"] = get_expected_badge_data(badge_1)
        expected_result["2"] = get_expected_badge_data(badge_2)

        actual_result = Badge.get_badges(community_type=TEAM_PLAYER[TEAM_PLAYER_ENTRY_INDEX])

        self.assertEqual(len(actual_result), len(expected_result))

        actual_result["1"] = actual_result.pop(actual_result.keys()[0])
        actual_result["2"] = actual_result.pop(actual_result.keys()[1])

        self.assertDictEqual(actual_result, expected_result)
