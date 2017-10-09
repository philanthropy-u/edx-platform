from optparse import make_option

from django.conf import settings
from django.contrib.auth.models import User

from student.models import UserProfile
from lms.djangoapps.onboarding_survey.models import (
    ExtendedProfile,
    OrganizationSurvey,
    InterestsSurvey,
    UserInfoSurvey,
    Organization
)
from track.management.tracked_command import TrackedCommand


class Command(TrackedCommand):
    help = """
    This command creates profiles according to 'ExtendedProfile' model for users.

    Due to the changes in database, previously registered users don't have extended profiles which gives
    server error. The purpose of this command is to create extended profiles to prevent server error.

    example:
        manage.py ... fix_broken_profiles
    """

    def are_surveys_complete(self, user):
        """
        Checks whether surveys are complete or not.

        There are three surveys, user info, interests and organization survey.
        This function returns true iff user has entries for all these surveys.

        Arguments:
            user(User): The user for which we want to check surveys

        Returns:
            boolean: True iff all surveys are complete.
        """
        surveys_are_complete = True
        try:
            user.user_info_survey
            user.interest_survey
            user.organization_survey
        except (UserInfoSurvey.DoesNotExist, InterestsSurvey.DoesNotExist, OrganizationSurvey.DoesNotExist):
            surveys_are_complete = False

        return surveys_are_complete

    def get_first_and_last_name(self, name):
        """
        Splits name on space and returns the values

        In case there are more than one spaces, we ignore all values
        except the first and last. If there is no space, then, both,
        first name and last name, would be equal to name.

        Arguments:
            name(str): The full name.

        Returns:
            list: A list containing first name and last name(in the same order).
        """
        name_splits = name.split(' ')
        if len(name_splits) == 2:
            return name_splits
        elif len(name_splits) > 2:
            return [name_splits[0], name_splits[-1]]
        else:
            return name_splits * 2

    def get_name(self, user):
        """
        Get the name of the user

        If user doesn't have profile attribute or profile has empty name then
        we use user's unique public username otherwise 'name' from user's profile.

        Arguments:
            user(User): The user of which to get the name

        Returns:
            str: The name of the user.
        """
        try:
            name = user.profile.name
            if not name:
                return user.username
            return name
        except UserProfile.DoesNotExist:
            return user.username

    def create_extended_profile(self, user):
        """
        Create extended profile for user

        Arguments:
            user(User): The user for which we want to create extended profile.
        """
        extended_profile = ExtendedProfile()
        first_name, last_name = self.get_first_and_last_name(self.get_name(user))

        extended_profile.user = user
        extended_profile.first_name = first_name
        extended_profile.last_name = last_name
        organization, created = Organization.objects.get_or_create(name='DummyOrg')
        extended_profile.organization = organization
        extended_profile.org_admin_email = ''
        extended_profile.is_survey_completed = self.are_surveys_complete(user)

        extended_profile.save()

    def create_user_profile(self, user):
        """
        Create edX's user profile for the user.

        Many features in the edX depend upon some of the fields in this model.

        Arguments:
            user(User): Django auth user model instance corresponding
                        the user of which to create the user profile.
        """
        user_profile = UserProfile()
        user_profile.name = user.username
        user_profile.user = user
        user_profile.save()

    def handle(self, *args, **options):

        users = User.objects.exclude(username__in=['honor', 'ecommerce_worker', 'verified', 'audit', 'user'])

        for user in users:
            try:
                user.extended_profile
            except ExtendedProfile.DoesNotExist:

                self.create_extended_profile(user)

            try:
                user.profile
            except UserProfile.DoesNotExist:
                self.create_user_profile(user)
