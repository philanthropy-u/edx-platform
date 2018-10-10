import requests

from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

from student.models import UserProfile, Registration
from lms.djangoapps.onboarding.models import UserExtendedProfile, EmailPreference
from common.lib.nodebb_client.client import NodeBBClient


class UserDeletionTestCase(TestCase):
    """
    Tests whether all of user data is deleted to make the app GDPR compliant
    """
    username = "testuser"
    email = "test@email.com"

    def setUp(self):
        user = User(
            username=self.username,
            email=self.email,
        )
        user.set_password("Arbisoft2")
        user.save()

        user_data = {
            'edx_user_id': user.id,
            'email': user.email,
            'first_name': "Test",
            'last_name': "User",
            'username': user.username,
            'date_joined': user.date_joined.strftime('%d/%m/%Y'),
        }
        NodeBBClient().users.create(username=user.username, user_data=user_data)

        email_preference = EmailPreference(
            user=user,
            opt_in="no",

        )
        email_preference.save()

        user_profile = UserProfile(
            user=user,
            name="Test User",
            level_of_education='b',
        )
        user_profile.save()

        extended_profile = UserExtendedProfile(
            user=user,
            is_interests_data_submitted=True,
            english_proficiency="Master",
        )
        extended_profile.save()

    def test_user_data_is_deleted(self):
        """
        Tests whether all the relevant user data is created
        """
        user = User.objects.filter(username=self.username).first()
        email_preference = EmailPreference.objects.filter(user=user).first()
        user_profile = UserProfile.objects.filter(user=user).first()
        extended_profile = UserExtendedProfile.objects.filter(
            user=user).first()

        data_endpoint = settings.NODEBB_ENDPOINT + '/api/v2/users/data'
        headers = {'Authorization': 'Bearer ' + settings.NODEBB_MASTER_TOKEN}
        response = requests.post(data_endpoint,
                                 data={'_uid': 1, 'username': self.username},
                                 headers=headers
                                )

        self.assertNotEqual(user, None)
        self.assertNotEqual(email_preference, None)
        self.assertNotEqual(user_profile, None)
        self.assertNotEqual(extended_profile, None)
        self.assertEqual(response.status_code, 200)

        historical_user_data = User.objects.raw(
            'SELECT * FROM auth_historicaluser WHERE email="{}";'.format(user.email))
        self.assertGreater(sum(1 for row in historical_user_data), 0)

        historical_user_profile_data = UserProfile.objects.raw(
            'SELECT * FROM auth_historicaluserprofile WHERE user_id={};'.format(user.id))
        self.assertGreater(sum(1 for row in historical_user_profile_data), 0)

        historical_user_extended_profile_data = UserExtendedProfile.objects.raw(
            'SELECT * from onboarding_historicaluserextendedprofile WHERE user_id={};'.format(user.id))
        self.assertGreater(
            sum(1 for row in historical_user_extended_profile_data), 0)

        user_id = user.id
        user.delete()

        email_preference = EmailPreference.objects.filter(user=user).first()
        user_profile = UserProfile.objects.filter(user=user).first()
        extended_profile = UserExtendedProfile.objects.filter(
            user=user).first()

        self.assertEqual(email_preference, None)
        self.assertEqual(user_profile, None)
        self.assertEqual(extended_profile, None)


        historical_user_data = User.objects.raw(
            'SELECT * FROM auth_historicaluser WHERE email="{}";'.format(user.email))
        self.assertEqual(sum(1 for row in historical_user_data), 0)

        historical_user_profile_data = UserProfile.objects.raw(
            'SELECT * FROM auth_historicaluserprofile WHERE user_id={};'.format(user_id))
        self.assertEqual(sum(1 for row in historical_user_profile_data), 0)

        historical_user_extended_profile_data = UserExtendedProfile.objects.raw(
            'SELECT * from onboarding_historicaluserextendedprofile WHERE user_id={};'.format(user_id))
        self.assertEqual(
            sum(1 for row in historical_user_extended_profile_data), 0)

        response = requests.post(data_endpoint,
                                 data={'_uid': 1, 'username': self.username},
                                 headers=headers
                                )
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        user = User.objects.filter(username=self.username).first()
        email_preference = EmailPreference.objects.filter(user=user).first()
        user_profile = UserProfile.objects.filter(user=user).first()
        extended_profile = UserExtendedProfile.objects.filter(
            user=user).first()

        if user:
            user.delete()
        if email_preference:
            email_preference.delete()
        if user_profile:
            user_profile.delete()
        if extended_profile:
            extended_profile.delete()

        NodeBBClient().users.delete_user(username=self.username)
