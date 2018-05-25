import json
from enrollment.api import get_enrollments
from mailchimp_pipeline.client import ChimpClient, MailChimpException
from mailchimp_pipeline.tasks import update_org_details_at_mailchimp
from lms.djangoapps.onboarding.models import (UserExtendedProfile, FocusArea, OrgSector, Organization,)
from lms.djangoapps.certificates import api as certificate_api
from student.models import (UserProfile, CourseEnrollment, )
from django.conf import settings

from logging import getLogger
log = getLogger(__name__)


def send_user_profile_info_to_mailchimp(sender, instance, kwargs):  # pylint: disable=unused-argument, invalid-name
    """ Create user account at nodeBB when user created at edx Platform """
    user_json = None
    if sender == UserProfile:
        profile = instance
        user_json = {
            "merge_fields": {
                "LANG": profile.language if profile.language else "",
                "COUNTRY": profile.country.name.format() if profile.country else "",
                "CITY": profile.city if profile.city else "",
            }
        }
    elif sender == UserExtendedProfile:
        extended_profile = instance
        user_json = {
            "merge_fields": {
                "ORG": extended_profile.organization.label if extended_profile.organization else ""
            }
        }
    elif sender == Organization:
        update_org_details_at_mailchimp.delay(instance.label, settings.MAILCHIMP_LEARNERS_LIST_ID)

    if user_json and not sender == Organization:
        try:
            response = ChimpClient().add_update_member_to_list(settings.MAILCHIMP_LEARNERS_LIST_ID, instance.user.email, user_json)
            log.info(response)
        except MailChimpException as ex:
            log.exception(ex)


def send_user_info_to_mailchimp(sender, user, created, kwargs):
    """ Create user account at nodeBB when user created at edx Platform """

    user_json = {
        "merge_fields": {
            "FULLNAME": user.get_full_name(),
            "USERNAME": user.username
        }
    }

    if created:
        user_json["merge_fields"].update({"DATEREGIS": str(user.date_joined.strftime("%m/%d/%Y"))})
        user_json.update({
            "email_address": user.email,
            "status_if_new": "subscribed"
        })
    try:
        response = ChimpClient().add_update_member_to_list(settings.MAILCHIMP_LEARNERS_LIST_ID, user.email, user_json)
        log.info(response)
    except MailChimpException as ex:
        log.exception(ex)


def send_user_enrollments_to_mailchimp(sender, instance, created, kwargs):
    user_json = {
        "merge_fields": {
            "ENROLLS": json.dumps([{"course_id": enrollment.get('course_details', {}).get('course_id', ''),
                                    "course_name": enrollment.get('course_details', {}).get('course_name', '')}
                                   for enrollment in get_enrollments(instance.user.username)]),
        }
    }
    try:
        response = ChimpClient().add_update_member_to_list(settings.MAILCHIMP_LEARNERS_LIST_ID, instance.user.email, user_json)
        log.info(response)
    except MailChimpException as ex:
        log.exception(ex)


def send_user_course_completions_to_mailchimp(sender, user, course_key, kwargs):
    all_certs = []
    try:
        all_certs = certificate_api.get_certificates_for_user(user.username)
    except:
        pass

    user_json = {
        "merge_fields": {
            "COMPLETES": json.dumps([{"course_id": cert.get('course_key', {}).__str__(),
                                    "course_name": cert.get('course_key', {}).course} for cert in all_certs
                                     if certificate_api.is_passing_status(cert['status'])]),
        }
    }
    try:
        response = ChimpClient().add_update_member_to_list(settings.MAILCHIMP_LEARNERS_LIST_ID, user.email, user_json)
        log.info(response)
    except MailChimpException as ex:
        log.exception(ex)
