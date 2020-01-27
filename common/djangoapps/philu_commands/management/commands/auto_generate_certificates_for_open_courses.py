"""
Django management command to auto generate certificates for all users
enrolled in currently running courses with early_no_info or early_with_info set
in the certificate_display_behavior setting in course advanced settings
"""

from logging import getLogger

from django.core.management.base import BaseCommand

from datetime import datetime
from django.apps import apps
from opaque_keys.edx.keys import UsageKey

from courseware.views.views import _get_cert_data
from lms.djangoapps.certificates.models import CertificateStatuses
from lms.djangoapps.certificates.api import generate_user_certificates
from student.models import CourseEnrollment
from xmodule.modulestore.django import modulestore

log = getLogger(__name__)

CERT_GENERATION_RESPONSE_MESSAGE = 'Generating certificate for user with ' \
                                   'username: {} and user_id: {} with ' \
                                   'generation status: {}'

StudentModule = apps.get_model('courseware', 'StudentModule')
GeneratedCertificate = apps.get_model('certificates', 'GeneratedCertificate')


def is_course_valid_for_certificate_auto_generation(course):
    return bool(course.has_started() and not course.has_ended() and course.may_certify())


def is_eligible_for_certificate(user_course_enrollment,
                                course_chapters, user):
    COURSE_STRUCTURE_INDEX = 0
    ESTIMATED_MODULE_COMPLETION_DAYS = 7
    today = datetime.utcnow()
    delta_days = (today - user_course_enrollment.created.date()).days
    total_modules = len(course_chapters[COURSE_STRUCTURE_INDEX].children)
    last_module_id = str(course_chapters[COURSE_STRUCTURE_INDEX].children[-1])
    usage_key = UsageKey.from_string(last_module_id)
    is_lastmodule_visitied = StudentModule.objects.filter(student=user, module_state_key=usage_key).exists()
    return ((total_modules - 1) * ESTIMATED_MODULE_COMPLETION_DAYS) >= delta_days and not is_lastmodule_visitied


class Command(BaseCommand):
    help = """
    The purpose of this command is to automatically generate certificates for
    all passed users (that do not have a certificate yet) in all currently
    running courses that have "certificate_display_behavior" set as
    "early_no_info" or "early_with_info"

    example:
        manage.py ... auto_generate_certificates_for_open_courses
    """

    def handle(self, *args, **options):
        for course in modulestore().get_courses():
            if not is_course_valid_for_certificate_auto_generation(course):
                continue

            for user_course_enrollment in CourseEnrollment.objects.filter(course=course.id, is_active=True).all():
                user = user_course_enrollment.user
                cert_data = _get_cert_data(user, course, user_course_enrollment.mode)
                if not cert_data or cert_data.cert_status != CertificateStatuses.requesting:
                    continue
                course_chapters = modulestore().get_items(
                    course.id,
                    qualifiers={'category': 'course'}
                )

                if is_eligible_for_certificate(user_course_enrollment, course_chapters, user):
                    continue

                '''
                    generate_user_certificates will add a request to xqueue to generate a new certificate for the user.
                    send_email=True parameter will let the callback url know to send email notification to the user as well.
                '''
                status = generate_user_certificates(user, course.id, course=course, send_email=True)
                log.info(CERT_GENERATION_RESPONSE_MESSAGE.format(user.username, user.id, status))
