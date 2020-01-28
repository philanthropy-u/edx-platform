from datetime import datetime

from lms.djangoapps.philu_overrides.constants import ACTIVATION_ALERT_TYPE
from pytz import utc

from constants import NON_ACTIVE_COURSE_NOTIFICATION
from student.models import CourseEnrollment
from courseware.models import StudentModule
from openedx.features.course_card.helpers import get_course_open_date
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from openedx.core.djangoapps.timed_notification.core import get_course_first_chapter_link


def get_non_active_course(user):
    DAYS_TO_DISPLAY_NOTIFICATION = 7

    all_user_courses = CourseEnrollment.objects.filter(user=user, is_active=True)

    non_active_courses = []
    non_active_course_info = []

    for user_course in all_user_courses:

        today = datetime.now(utc).date()

        try:
            course = CourseOverview.objects.get(id=user_course.course_id, end__gte=today)
        except CourseOverview.DoesNotExist:
            continue

        course_start_date = get_course_open_date(course).date()
        delta_date = today - course_start_date

        if delta_date.days >= DAYS_TO_DISPLAY_NOTIFICATION:

            modules = StudentModule.objects.filter(course_id=course.id, student_id=user.id,
                                                   created__gt=course_start_date)

            # Make this check equals to zero to make it more generic.
            if len(modules) <= 0:
                non_active_courses.append(course)

    if len(non_active_courses) > 0:
        error = NON_ACTIVE_COURSE_NOTIFICATION % (non_active_courses[0].display_name,
                                                  get_course_first_chapter_link(course=non_active_courses[0]))
        non_active_course_info.append({"type": ACTIVATION_ALERT_TYPE,
                                       "alert": error})
    return non_active_course_info


def get_register_form_data_override(pipeline_kwargs):
    """Gets dict of data to display on the register form.

    openedx.features.student_account.views.RegistrationViewCustom
    uses this to populate the new account creation form with values
    supplied by the user's chosen provider, preventing duplicate data entry.

    Args:
        pipeline_kwargs: dict of string -> object. Keyword arguments
            accumulated by the pipeline thus far.

    Returns:
        Dict of string -> string. Keys are names of form fields; values are
        values for that field. Where there is no value, the empty string
        must be used.
    """
    # Details about the user sent back from the provider.
    details = pipeline_kwargs.get('details')

    # Get the username separately to take advantage of the de-duping logic
    # built into the pipeline. The provider cannot de-dupe because it can't
    # check the state of taken usernames in our system. Note that there is
    # technically a data race between the creation of this value and the
    # creation of the user object, so it is still possible for users to get
    # an error on submit.
    suggested_username = pipeline_kwargs.get('username')

    return {
        'email': details.get('email', ''),
        'name': details.get('fullname', ''),
        'last_name': details.get('last_name', ''),
        'first_name': details.get('first_name', ''),
        'username': suggested_username,
    }
