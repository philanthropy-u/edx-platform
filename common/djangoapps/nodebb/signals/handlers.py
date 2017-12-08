from logging import getLogger

from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from common.lib.nodebb_client.client import NodeBBClient
from lms.djangoapps.onboarding.models import UserExtendedProfile
from nodebb.helpers import get_fields_to_sync_with_nodebb
from nodebb.models import DiscussionCommunity
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from student.models import ENROLL_STATUS_CHANGE, EnrollStatusChange, UserProfile
from xmodule.modulestore.django import modulestore

log = getLogger(__name__)


def log_action_response(user, status_code, response_body):
    if status_code != 200:
        log.error("Error: Can not update user(%s) on nodebb due to %s" % (user.username, response_body))
    else:
        log.info('Success: User(%s) has been created on nodebb' % user.username)


@receiver(post_save, sender=UserExtendedProfile)
@receiver(post_save, sender=User)
@receiver(post_save, sender=UserProfile)
def sync_user_info_with_nodebb(sender, instance, created, **kwargs):  # pylint: disable=unused-argument, invalid-name
    """
    Sync information b/w NodeBB User Profile and Edx User Profile, Surveys

    """

    fields_to_sync_with_nodebb = get_fields_to_sync_with_nodebb()

    if not kwargs['update_fields'] & set(fields_to_sync_with_nodebb):
        return

    user = None
    if sender in [UserProfile, UserExtendedProfile]:
        user = instance.user
    elif sender == User:
        user = instance

    if not created and user:
        # handle model update case
        if sender == User:
            data_to_sync = {
                "first_name": instance.first_name,
                "last_name": instance.last_name
            }
        elif sender == UserProfile:
            data_to_sync = {
                "city_of_residence": instance.city,
                "country_of_residence": instance.country,
                "birthday": "01/01/%s" % instance.year_of_birth,
                "language": instance.language,
            }
        elif sender == UserExtendedProfile:
            data_to_sync = {
                "country_of_employment": instance.country_of_employment,
                "city_of_employment": instance.city_of_employment,
                "interests": instance.get_user_selected_interests(),
                "focus_area": instance.get_user_selected_functions()
            }

            if instance.organization:
                data_to_sync["organization"] = instance.organization.label

        status_code, response_body = NodeBBClient().users.update_profile(user.username, kwargs=data_to_sync)
        log_action_response(user, status_code, response_body)

    elif created and sender == UserExtendedProfile:
        # handle user creation case
        data_to_sync = {
            'edx_user_id': instance.user.id,
            'email': instance.user.email,
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'username': instance.user.username,
            'date_joined': instance.user.date_joined.strftime('%d/%m/%Y'),
        }
        if instance.organization:
            data_to_sync["organization"] = instance.organization.label

        status_code, response_body = NodeBBClient().users.create(username=instance.user.username, kwargs=data_to_sync)
        log_action_response(user, status_code, response_body)

        return status_code


@receiver(pre_save, sender=User, dispatch_uid='activate_deactivate_user_on_nodebb')
def activate_deactivate_user_on_nodebb(sender, instance, **kwargs):
    """
    Activate or Deactivate a user on nodebb whenever user's active state changes on edx platform
    """
    current_user_obj = User.objects.filter(pk=instance.pk)

    if current_user_obj.first() and current_user_obj[0].is_active != instance.is_active:
        status_code, response_body = NodeBBClient().users.activate(username=instance.username,
                                                                   active=instance.is_active)

        if status_code != 200:
            log.error("Error: Can not change active status of a user(%s) on nodebb due to %s"
                      % (instance.username, response_body))
        else:
            log.info("Success: User(%s)'s active status('is_active:%s') has been changed on nodebb"
                     % (instance.username, instance.is_active))


@receiver(post_save, sender=CourseOverview, dispatch_uid="nodebb.signals.handlers.create_category_on_nodebb")
def create_category_on_nodebb(sender, instance, created, **kwargs):
    """
    Create a community on NodeBB whenever a new course is created
    """
    if created:
        community_name = '%s-%s-%s-%s' % (instance.display_name, instance.id.org, instance.id.course, instance.id.run)
        status_code, response_body = NodeBBClient().categories.create(name=community_name, label=instance.display_name)

        if status_code != 200:
            log.error(
                "Error: Can't create nodebb cummunity for the given course %s due to %s" % (
                    community_name, response_body
                )
            )
        else:
            DiscussionCommunity.objects.create(
                course_id=instance.id,
                community_url=response_body.get('categoryData', {}).get('slug')
            )
            log.info('Success: Community created for course %s' % instance.id)


@receiver(ENROLL_STATUS_CHANGE)
def join_group_on_nodebb(sender, event=None, user=None, **kwargs):  # pylint: disable=unused-argument
    """
    Automatically join a group on NodeBB [related to that course] on student enrollment
    """
    if event == EnrollStatusChange.enroll:
        user_name = user.username
        course = modulestore().get_course(kwargs.get('course_id'))

        community_name = '%s-%s-%s-%s' % (course.display_name, course.id.org, course.id.course, course.id.run)
        status_code, response_body = NodeBBClient().users.join(group_name=community_name, user_name=user_name)

        if status_code != 200:
            log.error(
                'Error: Can not join the group, user (%s, %s) due to %s' % (
                    course.display_name, user_name, response_body
                )
            )
        else:
            log.info('Success: User have joined the group %s successfully' % course.display_name)
