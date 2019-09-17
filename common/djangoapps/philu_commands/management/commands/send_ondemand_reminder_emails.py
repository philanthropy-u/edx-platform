import math
from pytz import utc
from datetime import datetime, timedelta
from logging import getLogger

from django.core.management.base import BaseCommand

from submissions.models import Submission
from common.lib.mandrill_client.client import MandrillClient
from student.models import CourseEnrollment

from xmodule.modulestore.django import modulestore
from openedx.core.djangoapps.content.course_structures.models import CourseStructure
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from openedx.features.courseware.helpers import get_nth_chapter_link
from openedx.features.ondemand_email_preferences.helpers import get_my_account_link
from lms.djangoapps.onboarding.helpers import get_email_pref_on_demand_course, get_user_anonymous_id

log = getLogger(__name__)

today = datetime.now().date()
DAYS_FOR_EACH_MODULE = 7
INACTIVITY_REMINDER_DAYS = 10
ORA_ASSESSMENT_BLOCK = 'openassessment'


class Command(BaseCommand):
    help = """
        Send reminder emails to those users who haven't completed the scheduled graded module for 10 days.
        This email will not be sent for those module which don't have at-least one graded sub-section.
    """

    def handle(self, *args, **options):

        # Getting all self paced courses.
        courses = CourseOverview.objects.filter(self_paced=True)

        for course in courses:
            try:
                course_struct = CourseStructure.objects.get(course_id=course.id).structure
            except CourseStructure.DoesNotExist:
                log.error('Course doesn\'t have a proper structure.')
                raise

            ora_blocks = get_all_oras(course_struct)

            # If course doesn't have any ORA blocks, continue.
            if not ora_blocks:
                continue

            course_blocks = course_struct['blocks']

            graded_oras_count = get_graded_ora_count(ora_blocks)
            last_module_oras = get_last_module_ora(course_blocks)

            # Getting all enrollments of user in self paced course.
            enrollments = CourseEnrollment.objects.filter(course_id=course.id, is_active=True)

            for enrollment in enrollments:
                user = enrollment.user

                try:
                    anonymous_user = get_user_anonymous_id(user, course.id)
                except Exception as error:
                    log.info(error)
                    continue

                # If user hasn't enable email preferences for on demand course, no need to go further.
                if not get_email_pref_on_demand_course(user, course.id):
                    continue

                course_chapters = modulestore().get_items(
                    course.id,
                    qualifiers={'category': 'course'}
                )

                course_deadline = get_course_deadline(enrollment.created.date(), course_chapters[0].children)

                # Get all user submission in descending order by date
                response_submissions = Submission.objects.filter(
                    student_item__student_id=anonymous_user.anonymous_user_id,
                    student_item__course_id=course.id.to_deprecated_string()).order_by('-created_at')

                # Check if user has submitted last modules graded oras or not. If yes not need to send email OR
                # If user's submission gets equal to graded oras count than don't need to continue..
                if (last_module_oras and check_for_last_module_submission(last_module_oras, anonymous_user)) or \
                        len(response_submissions) == graded_oras_count:
                    continue

                latest_submission = response_submissions.first()
                # Count to keep track of how many times user shows an inactivity for "INACTIVITY_REMINDER_DAYS"
                time_passed_count = 0

                if len(response_submissions) == 0 and is_time_passed(enrollment.created.date(), today):
                    send_reminder_email(user, course, course_deadline)
                    continue
                elif len(response_submissions) > 0:
                    # Check for latest submission entry from submission table if the difference of created date and
                    # today is equals to "INACTIVITY_REMINDER_DAYS" days this means that email should be send to user
                    # but before that we need to check is it the first time user shows an inactivity for
                    # "INACTIVITY_REMINDER_DAYS" days or not if yes than send email else means that emails has already
                    #  been sent to user so no need to send it again.
                    if is_time_passed(latest_submission.created_at.date(), today):
                        last_response_time = latest_submission.created_at.date()
                        # We have checked first entry separately so starting from second index.
                        for index_response, response in enumerate(response_submissions[1:]):
                            if is_time_passed(response.created_at.date(), last_response_time):
                                time_passed_count += 1
                        # If user haven't been inactive in past before today than send email.
                        if time_passed_count == 0:
                            send_reminder_email(user, course, course_deadline)
                    else:
                        continue


def is_time_passed(first_date, second_date):
    return True if (second_date - first_date).days == INACTIVITY_REMINDER_DAYS else False


def get_course_deadline(enrollment_date, chapters):
    return enrollment_date + timedelta(days=(len(chapters) * DAYS_FOR_EACH_MODULE))


def get_graded_ora_count(oras_block):
    graded_oras = []
    for ora in oras_block:
        if ora['graded']:
            graded_oras.append(ora)
    return len(graded_oras)


def get_all_oras(course_struct):
    ora_blocks = []
    for k, v in course_struct['blocks'].iteritems():
        if v['block_type'] == ORA_ASSESSMENT_BLOCK:
            ora_blocks.append(course_struct['blocks'][k])
    return ora_blocks


def get_last_module_ora(course_blocks):
    last_module_oras = []
    for index, block in course_blocks.iteritems():
        if block['block_type'] == 'course':
            course_children = block['children']
            final_chapter_index = len(course_children) - 1
            final_chapter_block = course_children[final_chapter_index]
            chapter_children = course_blocks[final_chapter_block]['children']
            for sequential in chapter_children:
                if course_blocks[sequential]['graded']:
                    sequential_children = course_blocks[sequential]['children']
                    for vertical in sequential_children:
                        for unit in course_blocks[vertical]['children']:
                            if course_blocks[unit]['block_type'] == ORA_ASSESSMENT_BLOCK:
                                last_module_oras.append(unit)

    return last_module_oras


def check_for_last_module_submission(oras_list, anonymous_user):
    for ora in oras_list:
        try:
            Submission.objects.get(
                student_item__student_id=anonymous_user.anonymous_user_id,
                student_item__item_id=ora)
        except Submission.DoesNotExist:
            return False
    else:
        return True


def send_reminder_email(user, course, course_deadline):
    """
        Send weekly emails for completed module

        Parameters:
        user: user, whom we are sending emails.
        course: Course for which we want to send email.
        course_deadline: Suggested deadline by which user must complete course.

        """
    template = MandrillClient.ON_DEMAND_REMINDER_EMAIL_TEMPLATE
    next_chapter_url = get_nth_chapter_link(course, chapter_index=1)
    context = {
        'first_name': user.first_name,
        'course_name': course.display_name,
        'deadline_date': str(course_deadline),
        'course_url': next_chapter_url,
        'email_address': user.email,
        'unsubscribe_link': get_my_account_link(course.id)
    }

    MandrillClient().send_mail(template, user.email, context)
    log.info("Emailing to %s Task Completed for course reminder", user.email)
