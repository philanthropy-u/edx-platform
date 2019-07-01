from __future__ import unicode_literals

import mock
from django.core.management import call_command
from django.db.models.signals import post_save
from django.test import TestCase
from factory.django import mute_signals
from lms.djangoapps.onboarding.helpers import COUNTRIES
from lms.djangoapps.onboarding.models import UserExtendedProfile
from lms.djangoapps.onboarding.tests.factories import UserFactory


class NodeBBSync(TestCase):
    """
        Tests for `create_certificates_image` command.
    """
    nodebb_data = {
        'website': '',
        'last_name': 'Test',
        'uid': 2,
        'first_name': 'Robot1',
        'country_of_residence': '',
        'email': 'test@example.com',
        'username': 'test',
        'city_of_residence': '',
        '_key': 'user:10',
        'country_of_employment': '',
        'fullname': 'Robot1 Test',
        'userslug': 'test',
        'edx_user_id': 2,
        'language': 'None'
    }

    @mute_signals(post_save)
    def setUp(self):
        super(NodeBBSync, self).setUp()
        self.user = UserFactory(username="test", email="test@example.com", password="123")
        self.user_edx_data = self._generate_edx_data()

    @mock.patch('common.lib.nodebb_client.users.ForumUser.all', return_value=[200, []])
    @mock.patch('common.djangoapps.nodebb.tasks.task_create_user_on_nodebb.delay')
    @mock.patch('common.djangoapps.nodebb.tasks.task_activate_user_on_nodebb.delay')
    def test_command_for_user_creation_on_nodebb(self, mocked_task_activate_user_on_nodebb,
                                                 mocked_task_create_user_on_nodebb,
                                                 mocked_all_func_nodebb_client_users_module):
        call_command('sync_users_with_nodebb')
        mocked_task_create_user_on_nodebb.assert_called_once_with(username=self.user.username,
                                                                  user_data=self.user_edx_data)
        mocked_task_activate_user_on_nodebb.assert_called_once_with(username=self.user.username,
                                                                    active=self.user.is_active)

    @mock.patch('common.djangoapps.nodebb.tasks.task_update_onboarding_surveys_status.delay')
    @mock.patch('lms.djangoapps.onboarding.models.UserExtendedProfile.unattended_surveys', return_value=[])
    @mock.patch('common.lib.nodebb_client.users.ForumUser.all', return_value=[200, []])
    @mock.patch('common.djangoapps.nodebb.tasks.task_create_user_on_nodebb.delay')
    @mock.patch('common.djangoapps.nodebb.tasks.task_activate_user_on_nodebb.delay')
    def test_command_for_user_creation_without_attended_surveys_on_nodebb(self, mocked_task_activate_user_on_nodebb,
                                                                          mocked_task_create_user_on_nodebb,
                                                                          mocked_all_func_nodebb_client_users_module,
                                                                          mocked_function_of_model,
                                                                          mocked_task_update_onboarding_surveys):
        call_command('sync_users_with_nodebb')
        mocked_task_create_user_on_nodebb.assert_called_once_with(username=self.user.username,
                                                                  user_data=self.user_edx_data)
        mocked_task_activate_user_on_nodebb.assert_called_once_with(username=self.user.username,
                                                                    active=self.user.is_active)
        mocked_task_update_onboarding_surveys.assert_called_once_with(username=self.user.username)

    @mock.patch('common.lib.nodebb_client.users.ForumUser.all', return_value=[302, []])
    def test_command_for_status_code_302(self, mocked_all_func_nodebb_client_users_module):
        self.assertIsNone(call_command('sync_users_with_nodebb'))

    @mock.patch('common.lib.nodebb_client.users.ForumUser.all', return_value=[200, [nodebb_data]])
    @mock.patch('common.djangoapps.nodebb.tasks.task_update_user_profile_on_nodebb.delay')
    def test_command_for_user_update_on_nodebb(self, mocked_task_update_user_profile_on_nodebbb,
                                               mocked_all_func_nodebb_client_users_module):
        call_command('sync_users_with_nodebb')
        mocked_task_update_user_profile_on_nodebbb.assert_called_once_with(username=self.user.username,
                                                                           profile_data=self.user_edx_data)

    @staticmethod
    def _generate_edx_data():
        extended_profile = UserExtendedProfile.objects.all()[0]
        user = extended_profile.user
        profile = user.profile

        edx_data = {
            'edx_user_id': unicode(user.id),
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'country_of_employment': extended_profile.country_of_employment,
            'city_of_employment': extended_profile.city_of_employment,
            'country_of_residence': COUNTRIES.get(profile.country.code),
            'city_of_residence': profile.city,
            'birthday': profile.year_of_birth,
            'language': profile.language,
            'interests': extended_profile.get_user_selected_interests(),
            'self_prioritize_areas': extended_profile.get_user_selected_functions()
        }

        return edx_data
