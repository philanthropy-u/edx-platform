from crum import get_current_request
from openedx.core.djangoapps.timed_notification.core import get_course_link
from student.models import ENROLL_STATUS_CHANGE, EnrollStatusChange
from lms.djangoapps.philu_api.helpers import get_course_custom_settings
from xmodule.modulestore.django import modulestore
from django.dispatch import receiver
from common.lib.mandrill_client.client import MandrillClient
from django.conf import settings

DEFAULT_DAYS_MODULE_COMPLETION = 7
ON_DEMAND_MODULE_TEXT = "<li> {module_name}: Complete by {module_comp_date}</li>"


@receiver(ENROLL_STATUS_CHANGE)
def enrollment_confirmation(sender, event=None, user=None, **kwargs):
    if event == EnrollStatusChange.enroll:
        course = modulestore().get_course(kwargs.get('course_id'))

        is_enrollment_email_enabled = True
        custom_settings = get_course_custom_settings(course.id)
        if custom_settings:
            is_enrollment_email_enabled = custom_settings.enable_enrollment_email

        template = None
        context = {
            'course_name': course.display_name,
            # TODO: find a way to move this code to PhilU overrides
            'course_url': get_course_link(course_id=course.id),
        }

        if is_enrollment_email_enabled and not course.self_paced:
            template = MandrillClient.ENROLLMENT_CONFIRMATION_TEMPLATE
            context.update(
                {'signin_url': settings.LMS_ROOT_URL + '/login',
                 'full_name': user.first_name + " " + user.last_name}
            )
        elif is_enrollment_email_enabled and course.self_paced:
            template = MandrillClient.ON_DEMAND_SCHEDULE_EMAIL
            context.update(
                {'module_list': get_chapters_text(course.id, user),
                 'first_name': user.first_name}
            )

        if template is not None:
            MandrillClient().send_mail(
                template,
                user.email,
                context,
                subject=('Welcome to %s!' % course.display_name)
                if template == MandrillClient.ON_DEMAND_SCHEDULE_EMAIL else None
            )


def get_chapters_text(course_id, user):
    from datetime import datetime
    from pytz import utc

    from openedx.features.course_card.helpers import get_course_open_date
    from lms.djangoapps.courseware.courses import get_course_with_access
    from lms.djangoapps.courseware.module_render import toc_for_course

    course = get_course_with_access(user, 'load', course_id, depth=2)
    # We don't need 'chapter_url_name', 'section_url_name' and 'field_
    # data_cache' to get list of modules so we passing None for these arguments.
    table_of_contents = toc_for_course(user, get_current_request(), course, None, None, None, )

    today = datetime.now(utc).date()
    course_start_date = get_course_open_date(course).date()
    delta_date = today - course_start_date

    if delta_date.days > 0:
        course_start_date = today

    chapters_text = ''
    module_comp_days = DEFAULT_DAYS_MODULE_COMPLETION
    for chapter in table_of_contents['chapters']:
        module_text = ON_DEMAND_MODULE_TEXT.format(
            module_name=chapter['display_name'],
            module_comp_date=get_next_date(course_start_date, module_comp_days)
        )
        chapters_text = chapters_text + module_text
        module_comp_days = module_comp_days + DEFAULT_DAYS_MODULE_COMPLETION
    return chapters_text


def get_next_date(today, module_date):
    from datetime import timedelta
    return str(today + timedelta(days=module_date))
