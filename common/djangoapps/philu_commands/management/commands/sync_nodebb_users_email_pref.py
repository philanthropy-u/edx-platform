"""
Django management command to create users at nodeBB corresponding to edx-platform users.
"""
from django.core.management.base import BaseCommand

from common.lib.nodebb_client.client import NodeBBClient
from lms.djangoapps.onboarding.models import EmailPreference
from nodebb.signals.handlers import log_action_response


class Command(BaseCommand):
    def handle(self, *args, **options):
        user_email_prefs = EmailPreference.objects.all()

        for pref in user_email_prefs:
            if pref.opt_in in ["yes", "no"]:
                data_to_sync = {
                    'emailPreferenceSet': 1,
                }
                status_code, response_body = NodeBBClient().users.update_profile(pref.user.username,
                                                                                 kwargs=data_to_sync)
                log_action_response(pref.user, status_code, response_body)
