from django.contrib.auth.models import User
from django.test import TestCase

from common.djangoapps.nodebb.constants import (
    TEAM_PLAYER_ENTRY_INDEX,
    CONVERSATIONALIST_ENTRY_INDEX
)

from openedx.features.badging.constants import CONVERSATIONALIST, TEAM_PLAYER
from openedx.features.badging.models import Badge

from openedx.features.badging.tests.factories import BadgeFactory


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

    def test_get_badges_json(self):
        """
        Check if get_badges_json returns correct json
        """
        expected_result = '[]'
        returned_result = Badge.get_badges_json(badge_type="no_match_")
        self.assertEqual(expected_result, returned_result)
