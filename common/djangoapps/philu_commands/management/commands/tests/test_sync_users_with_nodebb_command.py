from __future__ import unicode_literals

import mock
from django.core.management import call_command
from django.db.models.signals import post_save
from django.test import TestCase
from factory.django import mute_signals
from lms.djangoapps.onboarding.helpers import COUNTRIES
from lms.djangoapps.onboarding.models import UserExtendedProfile
from lms.djangoapps.onboarding.tests.factories import UserFactory

HTTP_SUCCESS = 200
HTTP_NOT_FOUND = 404


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
        self.user_edx_data = self._generate_edx_user_data()
        patcher = mock.patch('common.lib.nodebb_client.users.ForumUser.all')
        self.mocked_nodebb_response = patcher.start()
        self.addCleanup(patcher.stop)

    @mock.patch('common.djangoapps.nodebb.tasks.task_create_user_on_nodebb.delay')
    @mock.patch('common.djangoapps.nodebb.tasks.task_activate_user_on_nodebb.delay')
    def test_sync_users_with_nodebb_command_for_user_creation(self, mocked_task_activate_user_on_nodebb,
                                                              mocked_task_create_user_on_nodebb):
        """
        This test case is responsible for testing the user creation and activation part of command.

        :param mocked_task_activate_user_on_nodebb: Mocked task which takes data from command and send to nodebb.
        :param mocked_task_create_user_on_nodebb: Mocked task which takes data from command and send to nodebb.
        :return:
        """
        self.mocked_nodebb_response.return_value = [HTTP_SUCCESS, []]
        call_command('sync_users_with_nodebb')
        mocked_task_create_user_on_nodebb.assert_called_once_with(username=self.user.username,
                                                                  user_data=self.user_edx_data)
        mocked_task_activate_user_on_nodebb.assert_called_once_with(username=self.user.username,
                                                                    active=self.user.is_active)

    @mock.patch('common.djangoapps.nodebb.tasks.task_update_onboarding_surveys_status.delay')
    @mock.patch('lms.djangoapps.onboarding.models.UserExtendedProfile.unattended_surveys', return_value=[])
    @mock.patch('common.djangoapps.nodebb.tasks.task_create_user_on_nodebb.delay')
    @mock.patch('common.djangoapps.nodebb.tasks.task_activate_user_on_nodebb.delay')
    def test_sync_users_with_nodebb_command_without_attended_surveys(self, mocked_task_activate_user_on_nodebb,
                                                                     mocked_task_create_user_on_nodebb,
                                                                     mocked_function_of_model,
                                                                     mocked_task_update_onboarding_surveys):
        """
        This test case is responsible for testing and the user creation and updating the onboarding survey status
        on nodebb if it doesn't have attended any onboarding surveys.

        :param mocked_task_activate_user_on_nodebb: Mocked task which takes data from command and send to nodebb.
        :param mocked_task_create_user_on_nodebb: Mocked task which takes data from command and send to nodebb.
        :param mocked_function_of_model: Mocked function of Extended Profile to return Null.
        :param mocked_task_update_onboarding_surveys: Mocked task which takes data from command and send to nodebb.
        :return:
        """
        self.mocked_nodebb_response.return_value = [HTTP_SUCCESS, []]
        call_command('sync_users_with_nodebb')
        mocked_task_create_user_on_nodebb.assert_called_once_with(username=self.user.username,
                                                                  user_data=self.user_edx_data)
        mocked_task_activate_user_on_nodebb.assert_called_once_with(username=self.user.username,
                                                                    active=self.user.is_active)
        mocked_task_update_onboarding_surveys.assert_called_once_with(username=self.user.username)

    def test_sync_users_with_nodebb_command_for_bad_request_code(self):
        """
        This test case is responsible for testing the scenario when nodebb returns bad_request. In that case command
        Log the Issue and Terminate and returns nothing.
        """
        self.mocked_nodebb_response.return_value = [HTTP_NOT_FOUND, []]
        self.assertIsNone(call_command('sync_users_with_nodebb'))

    @mock.patch('common.djangoapps.nodebb.tasks.task_update_user_profile_on_nodebb.delay')
    def test_sync_users_with_nodebb_command_for_user_update(self, mocked_task_update_user_profile_on_nodebbb):
        """
        This test case is responsible for testing the user update part of command. This scenario is generated when a
        user is already generated on nodebb and later user settings(name, date_birth, etc) are updated on edX.

        :param mocked_task_update_user_profile_on_nodebbb: Mocked task which takes data from command and send to nodebb.
        """
        self.mocked_nodebb_response.return_value = [HTTP_SUCCESS, [self.nodebb_data]]
        call_command('sync_users_with_nodebb')
        mocked_task_update_user_profile_on_nodebbb.assert_called_once_with(username=self.user.username,
                                                                           profile_data=self.user_edx_data)

    def _generate_edx_user_data(self):
        """
        This function will generate data we send to nodebb for users.
        """
        extended_profile = UserExtendedProfile.objects.all()[0]
        user = extended_profile.user
        profile = user.profile

        edx_user_data = {
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

        return edx_user_data
