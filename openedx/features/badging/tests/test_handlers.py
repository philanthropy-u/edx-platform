from django.test import TestCase
from edx_notifications.exceptions import ItemNotFoundError
from edx_notifications.lib.publisher import get_notification_type

from openedx.features.badging.constants import EARNED_BADGE_NOTIFICATION_TYPE, JSON_NOTIFICATION_RENDERER

from .. import handlers as badge_handlers


class BadgeHandlerTestCase(TestCase):

    def test_register_notification_types(self):
        """
        Test that notification type is registered correctly
        :return: None
        """
        # register badge notification type
        badge_handlers.register_notification_types(None)

        badge_notification_type = get_notification_type(EARNED_BADGE_NOTIFICATION_TYPE)

        self.assertEqual(badge_notification_type.name, EARNED_BADGE_NOTIFICATION_TYPE)
        self.assertEqual(badge_notification_type.renderer, JSON_NOTIFICATION_RENDERER)

    def test_register_notification_types_error(self):
        """
        Test that ItemNotFoundError exception is raised if invalid notification
        type is accessed from store
        :return: None
        """

        with self.assertRaises(ItemNotFoundError) as not_found_error:
            get_notification_type("invalid")

        self.assertEqual(not_found_error.exception.message, "")
