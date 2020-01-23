"""
Signal handlers for the bulk_email app
"""

from django.dispatch import receiver

from student.models import CourseEnrollment
import logging
from common.lib.mandrill_client.client import MandrillClient
from openedx.core.djangoapps.user_api.accounts.signals import USER_RETIRE_MAILINGS, USER_CERTIFICATE_DOWNLOADABLE

from .models import Optout

log = logging.getLogger(__name__)

@receiver(USER_RETIRE_MAILINGS)
def force_optout_all(sender, **kwargs):  # pylint: disable=unused-argument
    """
    When a user is retired from all mailings this method will create an Optout
    row for any courses they may be enrolled in.
    """
    user = kwargs.get('user', None)

    if not user:
        raise TypeError('Expected a User type, but received None.')

    for enrollment in CourseEnrollment.objects.filter(user=user):
        Optout.objects.get_or_create(user=user, course_id=enrollment.course.id)


@receiver(USER_CERTIFICATE_DOWNLOADABLE)
def send_email_user_certificate_downloadable(sender, first_name, display_name, certificate_reverse_url, user_email,
                                             *args, **kwargs):
    template = MandrillClient.DOWNLOAD_CERTIFICATE

    context = dict(first_name=first_name, course_name=display_name,
                   certificate_url=certificate_reverse_url)
    try:
        MandrillClient().send_mail(template, user_email, context)
    except Exception as e:
        # Mandrill errors are thrown as exceptions
        log.error('Unable to send email for USER_CERTIFICATE_DOWNLOADABLE signal: %s - %s' % (e.__class__, e))
