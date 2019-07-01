from __future__ import unicode_literals

import logging

import mock
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.db.models.signals import post_save
from django.test import TestCase
from factory.django import mute_signals
from lms.djangoapps.certificates import api as certificate_api
from lms.djangoapps.onboarding.models import FocusArea, OrgSector
from lms.djangoapps.onboarding.tests.factories import OrganizationFactory, UserFactory
from mailchimp_pipeline.helpers import get_enrollements_course_short_ids, get_user_active_enrollements
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview

log = logging.getLogger(__name__)
logging.disable(logging.NOTSET)
log.setLevel(logging.DEBUG)


class MailChimpUser(TestCase):
    """
        Tests for both `sync_users_with_mailchimp` and `delete_users_from_mailchimp` command.
    """

    @mute_signals(post_save)
    def setUp(self):
        super(MailChimpUser, self).setUp()
        self.user = UserFactory.create(
            username="test",
            password="test123",
            email="test@example.com"
        )
        org = OrganizationFactory()
        org.org_type = "New"
        org.save()
        self.user.extended_profile.organization = org
        self.user.extended_profile.save()

    @mock.patch('mailchimp_pipeline.client.ChimpClient.delete_user_from_list')
    def test_delete_users_from_mailchimp(self, mock_func):
        call_command('delete_users_from_mailchimp')
        mock_func.assert_called_once_with(settings.MAILCHIMP_LEARNERS_LIST_ID, self.user.email)

    @mock.patch('mailchimp_pipeline.client.ChimpClient.add_list_members_in_batch')
    @mock.patch('django.db.connection')
    def test_sync_users_with_mailchimp_command(self, mocked_connection, mock_func):
        users = list(User.objects.all())
        users_data = self.get_users_data_to_send(users)
        call_command('sync_users_with_mailchimp')
        mock_func.assert_called_once_with(settings.MAILCHIMP_LEARNERS_LIST_ID, {"members": users_data})

    @mock.patch('lms.djangoapps.certificates.api.get_certificates_for_user')
    @mock.patch('mailchimp_pipeline.client.ChimpClient.add_list_members_in_batch')
    @mock.patch('django.db.connection')
    def test_sync_users_with_mailchimp_command_for_cert_exception(self, mocked_connection, mock_func,
                                                                  mocked_get_user_cert_func):
        mocked_get_user_cert_func.side_effect = Exception
        users = list(User.objects.all())
        users_data = self.get_users_data_to_send(users)
        call_command('sync_users_with_mailchimp')
        mock_func.assert_called_once_with(settings.MAILCHIMP_LEARNERS_LIST_ID, {"members": users_data})
        self.assertRaises(Exception)

    @mock.patch('django.db.connection')
    def test_sync_users_with_mailchimp_command_for_exception(self, mocked_connection):
        users = list(User.objects.all())
        users_data = self.get_users_data_to_send(users)
        call_command('sync_users_with_mailchimp')
        self.assertRaises(Exception)

    @mock.patch('philu_commands.management.commands.sync_users_with_mailchimp.get_user_active_enrollements')
    @mock.patch('django.db.connection')
    def test_sync_users_with_mailchimp_command_for_user_exception(self, mocked_connection, mocked_user_enrollment_func):
        mocked_user_enrollment_func.side_effect = Exception
        users = list(User.objects.all())
        users_data = self.get_users_data_to_send(users)
        call_command('sync_users_with_mailchimp')
        self.assertRaises(Exception)

    def get_users_data_to_send(self, users):
        users_set = []

        focus_areas = FocusArea.get_map()
        org_sectors = OrgSector.get_map()

        for user in users:
            profile = user.profile
            extended_profile = user.extended_profile

            org_type = ""
            if extended_profile.organization and extended_profile.organization.org_type:
                org_type = org_sectors.get(extended_profile.organization.org_type, '')

            all_certs = []
            try:
                all_certs = certificate_api.get_certificates_for_user(user.username)
            except Exception as ex:
                log.exception(str(ex.args))

            completed_course_keys = [cert.get('course_key', '') for cert in all_certs
                                     if certificate_api.is_passing_status(cert['status'])]
            completed_courses = CourseOverview.objects.filter(id__in=completed_course_keys)

            try:
                user_json = {
                    "email_address": user.email,
                    "status_if_new": "subscribed",
                    "merge_fields": {
                        "FULLNAME": user.get_full_name(),
                        "USERNAME": user.username,
                        "LANG": profile.language if profile.language else "",
                        "COUNTRY": profile.country.name.format() if profile.country else "",
                        "CITY": profile.city if profile.city else "",
                        "DATEREGIS": str(user.date_joined.strftime("%m/%d/%Y")),
                        "LSOURCE": "",
                        "COMPLETES": ", ".join([course.display_name for course in completed_courses]),
                        "ENROLLS": get_user_active_enrollements(user.username),
                        "ENROLL_IDS": get_enrollements_course_short_ids(user.username),
                        "ORG": extended_profile.organization.label if extended_profile.organization else "",
                        "ORGTYPE": org_type,
                        "WORKAREA": str(focus_areas.get(extended_profile.organization.focus_area, ""))
                        if extended_profile.organization else "",
                    }
                }
            except Exception as ex:
                log.info("There was an error for user with email address as {}".format(user.email))
                log.exception(str(ex.args))
                continue

            users_set.append(user_json)

        return users_set
