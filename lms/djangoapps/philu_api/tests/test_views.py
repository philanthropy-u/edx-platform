import json
from mock import patch

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase

from lms.djangoapps.philu_api.views import assign_user_badge


class BadgeAssignViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.assign_path = reverse('assign_user_badge')

    @patch('lms.djangoapps.philu_api.views.UserBadge.assign_badge')
    def test_assign_user_badge_wrong_token(self, mock_userbadge_assign_badge):
        dict_data = {
            "user_id": "16",
            "badge_id": "1",
            "community_id": "-1",
            "token": "wrong_token"
        }
        request = self.factory.post(self.assign_path, data=json.dumps(dict_data), content_type='application/json')

        response = assign_user_badge(request)

        assert not mock_userbadge_assign_badge.called

        self.assertEqual(response.status_code, 403)

    @patch('lms.djangoapps.philu_api.views.UserBadge.assign_badge')
    def test_assign_user_badge(self, mock_userbadge_assign_badge):
        dict_data = {
            "user_id": "16",
            "badge_id": "1",
            "community_id": "-1",
            "token": settings.NODEBB_MASTER_TOKEN
        }
        request = self.factory.post(self.assign_path, data=json.dumps(dict_data), content_type='application/json')

        response = assign_user_badge(request)

        assert mock_userbadge_assign_badge.called

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"success": true}')

    @patch('lms.djangoapps.philu_api.views.UserBadge.assign_badge')
    def test_assign_user_badge_exception(self, mock_userbadge_assign_badge):
        dict_data = {
            "user_id": "16",
            "badge_id": "1",
            "community_id": "-1",
            "token": settings.NODEBB_MASTER_TOKEN
        }
        request = self.factory.post(self.assign_path, data=json.dumps(dict_data), content_type='application/json')

        mock_userbadge_assign_badge.side_effect = Exception()
        response = assign_user_badge(request)

        assert mock_userbadge_assign_badge.called
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, '{"message": "", "success": false}')
