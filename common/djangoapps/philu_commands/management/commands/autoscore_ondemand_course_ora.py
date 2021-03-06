"""
Command to auto score ORA.
"""
from logging import getLogger

from django.core.management.base import BaseCommand
from openassessment.workflow.models import AssessmentWorkflow

from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from openedx.features.assessment.helpers import find_and_autoscore_submissions
from student.models import CourseEnrollment

log = getLogger(__name__)


class Command(BaseCommand):
    """
    Auto Score ORA assessment for on demand course
    """
    help = """
    Auto score ORA assessment of on demand course, if learner has submitted ORA a certain number of days ago. Number
    of days are configurable from site configurations model though its default value is 3 days.

    In-order to access site configurations, site id of LMS site is required as a command param, but if it is not
    provided or its value is wrong then default ORA assessment waiting value will be DAYS_TO_WAIT_AUTO_ASSESSMENT days.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '--site-id',
            action='store',
            dest='site_id',
            type=int,
            help='LMS site id, to get configuration from.'
        )

    def handle(self, *args, **options):
        site_id = options.get('site_id')

        ondemand_course_ids = CourseOverview.objects.filter(self_paced=True).values_list('id', flat=True)
        submission_uuids = AssessmentWorkflow.objects.filter(course_id__in=ondemand_course_ids).values_list(
            'submission_uuid', flat=True).exclude(status__in=['done', 'cancelled'])

        if not submission_uuids:
            log.info('No pending open response assessment found to autoscore. No ORA in progress')
            return

        enrollments = CourseEnrollment.objects.filter(course_id__in=ondemand_course_ids, is_active=True)

        find_and_autoscore_submissions(list(enrollments), list(submission_uuids), site_id)
