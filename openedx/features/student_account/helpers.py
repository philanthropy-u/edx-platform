from datetime import datetime
from pytz import utc

from student.models import CourseEnrollment
from courseware.models import StudentModule
from openedx.features.course_card.helpers import get_course_open_date
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from openedx.core.djangoapps.timed_notification.core import get_course_first_chapter_link


def get_non_active_course(user):

    DAYS_TO_DISPLAY_NOTIFICATION = 7

    all_user_courses = CourseEnrollment.objects.filter(user=user, is_active=True)

    active_courses = []
    overview_courses = []

    for user_course in all_user_courses:

        today = datetime.now(utc).date()

        course = CourseOverview.objects.get(id=user_course.course_id)

        if datetime.now(utc).date() > course.end.date():
            continue

        course_start_date = get_course_open_date(course).date()
        delta_date = today - course_start_date

        if delta_date.days >= DAYS_TO_DISPLAY_NOTIFICATION:

            overview_courses.append(course)
            modules = StudentModule.objects.filter(course_id=course.id)

            for mod_entry in modules:
                # Verifying if mod_entry is after Course Open date
                if course_start_date < mod_entry.created.date():
                    active_courses.append(course)
                    break

    non_active_courses = [course for course in overview_courses if course not in active_courses]

    first_non_active_course = {}
    if len(non_active_courses) > 0:
        first_non_active_course = {'course_name': non_active_courses[0].display_name,
                                   'course_link': get_course_first_chapter_link(course=non_active_courses[0])}
    return first_non_active_course
