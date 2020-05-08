from datetime import datetime

import pytz
from django.views.decorators.csrf import csrf_exempt

from course_action_state.models import CourseRerunState
from edxmako.shortcuts import render_to_response
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from openedx.features.course_card.models import CourseCard
from philu_overrides.helpers import get_user_current_enrolled_class
from student.models import CourseEnrollment

from ...core.djangoapps.catalog.utils import get_programs
from ..specializations.helpers import date_from_str
from .helpers import get_course_open_date

utc = pytz.UTC


def get_course_start_date(course):
    """
    this function takes course and returns start date of the course
    if start and end dates are set and start date is in future
    :param course:
    :return Course start date:
    """

    if course and course.start:
        return get_course_open_date(course)

    return None


@csrf_exempt
def get_course_cards(request):
    """
    :param request:
    :return: list of active cards
    """
    cards_query_set = CourseCard.objects.all() if request.user.is_staff else CourseCard.objects.filter(is_enabled=True)
    course_card_ids = [cc.course_id for cc in cards_query_set]
    courses_list = CourseOverview.objects.select_related('image_set').filter(id__in=course_card_ids)
    courses_list = sorted(courses_list, key=lambda _course: _course.number)
    current_time = datetime.utcnow()

    filtered_courses = []
    programs = get_programs(request.site)

    for course in courses_list:

        if course.invitation_only and not CourseEnrollment.is_enrolled(request.user, course.id):
            continue

        # check if any active (currently open or are starting in future)
        # run of a course is part of a program.
        course_program = [program for program in programs
                          for program_course in program['courses']
                          if program_course['course_runs']
                          and str(course.id) in [rerun['key'] for rerun in program_course['course_runs']
                                                 if rerun['enrollment_start'] and rerun['enrollment_end']
                                                 and (date_from_str(rerun['enrollment_start']) > current_time
                                                 or date_from_str(rerun['enrollment_start']) <= current_time <= date_from_str(rerun['enrollment_end']))]]

        course_rerun_states = [crs.course_key for crs in CourseRerunState.objects.filter(
            source_course_key=course.id, action="rerun", state="succeeded")]

        course_rerun_object = CourseOverview.objects.select_related('image_set').filter(
            id__in=course_rerun_states, enrollment_end__gte=current_time).order_by('enrollment_start').first()

        course = get_course_with_link_and_start_date(course, course_rerun_object, request, course_program)

        filtered_courses.append(course)

    return render_to_response(
        "course_card/courses.html",
        {
            'courses': filtered_courses
        }
    )


def get_course_with_link_and_start_date(course, course_rerun_object, request, course_program):
    date_time_format = '%b %-d, %Y'
    current_time = datetime.utcnow().replace(tzinfo=utc)

    current_class, user_current_enrolled_class, current_enrolled_class_target = get_user_current_enrolled_class(
        request, course)

    if current_class:
        current_class_start_date = get_course_open_date(current_class)

    course.specialization = any(course_program)

    if user_current_enrolled_class:
        course.is_enrolled = True
        course.course_target = current_enrolled_class_target
        course.start_date = current_class_start_date.strftime(date_time_format)
        course.self_paced = current_class.self_paced
        return course

    course_start_time = get_course_start_date(course)
    rerun_start_time = get_course_start_date(course_rerun_object)

    if course.enrollment_end:
        _enrollment_end_date = course.enrollment_end.replace(tzinfo=utc)
        if _enrollment_end_date > current_time:
            course.start_date = course_start_time.strftime(date_time_format)
            return course

    if course_rerun_object and course_rerun_object.enrollment_end:
        _enrollment_end_date = course_rerun_object.enrollment_end.replace(tzinfo=utc)
        if _enrollment_end_date > current_time:
            course.start_date = rerun_start_time.strftime(date_time_format)
            course.self_paced = course_rerun_object.self_paced
            return course

    if current_class:
        course.start_date = current_class_start_date.strftime(date_time_format)
        course.self_paced = current_class.self_paced
        return course

    course.start_date = None
    return course
