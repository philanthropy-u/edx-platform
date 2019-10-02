from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from common.djangoapps.nodebb.constants import (
    COMMUNITY_ID_SPLIT_INDEX,
    TEAM_PLAYER_ENTRY_INDEX,
    CONVERSATIONALIST_ENTRY_INDEX
)

from openedx.features.badging.constants import CONVERSATIONALIST, TEAM_PLAYER
from openedx.features.badging.models import Badge, UserBadge


class BadgeModelTestCases(TestCase):
    def test_name_blank_raises_IntegrityError(self):
        """
        Trying to save a Badge object with no name raises
        an IntegrityError exception.
        """
        badge = Badge(name=None,
                      description="This is a sample badge",
                      threshold=30,
                      type="conversationalist",
                      image="path/too/image",
                      date_created=timezone.now())

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                badge.save()
        badge.delete

    def test_description_blank_no_exception(self):
        """
        Trying to save a Badge object with no description
        does not raise any exception.
        """
        badge_name = "Sample Badge"
        badge = Badge(name=badge_name,
                      description=None,
                      threshold=30,
                      type="conversationalist",
                      image="path/too/image",
                      date_created=timezone.now())
        badge.save()
        saved_badge = Badge.objects.get(name=badge_name)
        self.assertEquals(badge, saved_badge)

    def test_threshold_blank_raises_IntegrityError(self):
        """
        Trying to save a Badge object with no threshold
        raises an IntegrityError exception.
        """
        badge = Badge(name="Sample Badge",
                      description="This is a sample badge",
                      threshold=None,
                      type="conversationalist",
                      image="path/too/image",
                      date_created=timezone.now())

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                badge.save()

    def test_type_blank_raises_IntegrityError(self):
        """
        Trying to save a Badge object with no type
        raises an IntegrityError exception.
        """
        badge = Badge(name="Sample Badge",
                      description="This is a sample badge",
                      threshold=30,
                      type=None,
                      image="path/too/image",
                      date_created=timezone.now())

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                badge.save()

    def test_image_blank_raises_IntegrityError(self):
        """
        Trying to save a Badge object with no image path
        raises an IntegrityError exception.
        """
        badge = Badge(name="Sample Badge",
                      description="This is a sample badge",
                      threshold=30,
                      type="conversationalist",
                      image=None,
                      date_created=timezone.now())

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                badge.save()

    def test_date_blank_sets_current_date(self):
        """
        Trying to save a Badge object with no date_created
        automatically sets it to current date.
        """
        badge_name = "Sample Badge"
        badge = Badge(name=badge_name,
                      description="This is a sample badge",
                      threshold=30,
                      type="conversationalist",
                      image="path/to/image",
                      date_created=None)
        time_at_save = timezone.now().replace(microsecond=0)
        badge.save()
        saved_time = Badge.objects.get(name=badge_name).date_created.replace(microsecond=0)

        self.assertEquals(time_at_save, saved_time)

    def test_save_badge_normal(self):
        """
        Trying to save a Badge object with all the right arguments.
        """
        badge = Badge(name="Sample Badge",
                      description="This is a sample badge",
                      threshold=30,
                      type="conversationalist",
                      image="path/to/image",
                      date_created=None)
        self.assertEqual(badge.save(), None)

    def test_remaining_badges_empty(self):
        """
        Get remaining badges dictionary without saving any
        badges earlier so nothing matches
        """
        expected_result = {}
        returned_result = Badge.get_unearned_badges(user_id=-1,
                                                    community_id=-1,
                                                    community_type="no_match_")
        self.assertEqual(expected_result, returned_result)

    def test_remaining_badges_none_earned(self):
        """
        Get remaining badges dictionary after saving badges
        when none of the badges has been earned
        """
        badge_1 = Badge(name="badge_1", description="This is a sample badge",
                        threshold=30, type="team", image="path/to/image")
        badge_1.save()
        badge_2 = Badge(name="badge_2", description="This is a sample badge",
                        threshold=70, type="team", image="path/to/image")
        badge_2.save()

        expected_result = {}
        expected_result["1"] = {'name': badge_1.name,
                                'description': badge_1.description,
                                'threshold': badge_1.threshold,
                                'type': badge_1.type,
                                'image': badge_1.image}
        expected_result["2"] = {'name': badge_2.name,
                                'description': badge_2.description,
                                'threshold': badge_2.threshold,
                                'type': badge_2.type,
                                'image': badge_2.image}

        actual_result = Badge.get_unearned_badges(user_id=-1,
                                                  community_id=-1,
                                                  community_type=TEAM_PLAYER[TEAM_PLAYER_ENTRY_INDEX])

        self.assertEqual(len(actual_result), len(expected_result))

        actual_result["1"] = actual_result.pop(actual_result.keys()[0])
        actual_result["2"] = actual_result.pop(actual_result.keys()[1])

        self.assertDictEqual(actual_result, expected_result)

    def test_remaining_badges_one_earned(self):
        """
        Get remaining badges dictionary after saving badges
        when user has already earned one of the badges
        """
        user = User.objects.create_user(username='testuser', password='12345')
        badge_1 = Badge(name="badge_1", description="This is a sample badge",
                        threshold=30, type="team", image="path/to/image")
        badge_1.save()
        badge_2 = Badge(name="badge_2", description="This is a sample badge",
                        threshold=70, type="team", image="path/to/image")
        badge_2.save()

        UserBadge.objects.create(
            user_id=user.id,
            badge_id=badge_1.id,
            course_id="",
            community_id=-1
        )

        expected_result = {}
        expected_result["1"] = {'name': badge_2.name,
                                'description': badge_2.description,
                                'threshold': badge_2.threshold,
                                'type': badge_2.type,
                                'image': badge_2.image}

        actual_result = Badge.get_unearned_badges(user_id=user.id,
                                                  community_id=-1,
                                                  community_type=TEAM_PLAYER[TEAM_PLAYER_ENTRY_INDEX])

        self.assertEqual(len(actual_result), len(expected_result))

        actual_result["1"] = actual_result.pop(actual_result.keys()[0])

        self.assertDictEqual(actual_result, expected_result)

    def test_remaining_badges_all_earned(self):
        """
        Get remaining badges dictionary after saving badges
        when user has already earned all of the badges
        """
        user = User.objects.create_user(username='testuser', password='12345')
        badge_1 = Badge(name="badge_1", description="This is a sample badge",
                        threshold=30, type="team", image="path/to/image")
        badge_1.save()
        badge_2 = Badge(name="badge_2", description="This is a sample badge",
                        threshold=70, type="team", image="path/to/image")
        badge_2.save()

        UserBadge.objects.create(
            user_id=user.id,
            badge_id=badge_1.id,
            course_id="",
            community_id=-1
        )

        UserBadge.objects.create(
            user_id=user.id,
            badge_id=badge_2.id,
            course_id="",
            community_id=-1
        )

        expected_result = {}
        actual_result = Badge.get_unearned_badges(user_id=user.id,
                                                  community_id=-1,
                                                  community_type=TEAM_PLAYER[TEAM_PLAYER_ENTRY_INDEX])

        self.assertEqual(len(actual_result), len(expected_result))
        self.assertDictEqual(actual_result, expected_result)
