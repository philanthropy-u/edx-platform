from common.lib.mandrill_client.client import MandrillClient
from courseware.models import StudentModule
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from openedx.core.djangoapps.timed_notification.core import get_course_link
from openedx.features.course_card.helpers import get_course_open_date
from student.models import CourseEnrollment
from django.core.management.base import BaseCommand
from openedx.features.course_card.models import CourseCard
from datetime import datetime, timedelta

from logging import getLogger
log = getLogger(__name__)


class Command(BaseCommand):
    help = """
    Send Notifications prompts to users who have not entered into course after enrollment.
    Orientation module will not be considered because that module will be accessible to user 
    before course actually starts. We are managing this by introducing our own date "Course Open Date"
    in custom setting.
    """

    def handle(self, *args, **options):
        courses = CourseCard.objects.all()

        for course in courses:
            course_overview = CourseOverview.get_from_id(course_id=course.course_id)

            today = datetime.now().date()
            log.info('Today date %s', today)

            course_start_date = get_course_open_date(course_overview).date()
            log.info('Course start date %s', course_start_date)

            delta_date = today - course_start_date
            log.info('Days passed since course started %s', delta_date.days)

            if delta_date.days == 7:

                log.info('Getting all enrollments for %s course', course_overview.display_name)
                all_enrollments = CourseEnrollment.objects.filter(course_id=course.course_id)

                active_users = []
                enrolled_users = []

                for enrollment in all_enrollments:
                    enrolled_users.append(enrollment.user)

                modules = StudentModule.objects.filter(course_id=course.course_id)

                for mod in modules:
                    if course_start_date < mod.created.date() <= (course_start_date + timedelta(days=7)):
                        active_users.append(mod.student)

                unique_users = [k for k in dict.fromkeys(active_users)]

                s = set(unique_users)
                non_actives = [x for x in enrolled_users if x not in s]

                for non_active_user in non_actives:
                    context = {}
                    first_name = non_active_user.first_name
                    course_name = course_overview.display_name
                    course_url = get_course_link(course_id=course_overview.id)

                    template = MandrillClient.COURSE_ACTIVATION_REMINDER
                    context = {
                        'first_name': first_name,
                        'course_name': course_name,
                        'course_url': course_url
                    }

                    MandrillClient().send_mail(template, non_active_user.email, context)
                    log.info('CELERY-TASK: date_now: %s, course_start_date: %s', today, course_start_date)

                    log.info("Emailing to %s Task Completed", non_active_user.email)
