from pytz import utc
from copy import deepcopy
from datetime import datetime

from . import helpers
from edxmako.shortcuts import render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required

from xmodule.error_module import ErrorDescriptor
from course_action_state.models import CourseRerunState, CourseRerunUIStateManager
from cms.djangoapps.contentstore.views.course import get_courses_accessible_to_user
from util.json_request import expect_json, JsonResponse


def latest_course_reruns(courses):
    """
    This method evaluates only the latest reruns of all given courses
    :param courses: list of courses to compute latest courses from
    :return: list of latest course reruns (CourseSummary Objects)
    """
    latest_courses_ids = set()

    for course in courses:
        course_rerun = CourseRerunState.objects.filter(course_key=course.id).first()
        is_course_parent_course = bool(
            CourseRerunState.objects.filter(source_course_key=course.id,
                                            state=CourseRerunUIStateManager.State.SUCCEEDED))

        if not course_rerun and not is_course_parent_course:
            latest_courses_ids.add(course.id)
            continue

        if is_course_parent_course:
            sibling_re_runs = CourseRerunState.objects.filter(
                source_course_key=course.id,
                state=CourseRerunUIStateManager.State.SUCCEEDED).order_by(
                '-created_time').all()
        else:
            sibling_re_runs = CourseRerunState.objects.filter(
                source_course_key=course_rerun.source_course_key,
                state=CourseRerunUIStateManager.State.SUCCEEDED).order_by(
                '-created_time').all()

        if sibling_re_runs:
            latest_courses_ids.add(sibling_re_runs[0].course_key)
        else:
            latest_courses_ids.add(course_rerun.course_key)

    return [course for course in courses if course.id in latest_courses_ids]


@expect_json
@login_required
@ensure_csrf_cookie
def course_multiple_rerun_handler(request):
    courses, in_process_course_actions = get_courses_accessible_to_user(request)
    in_process_action_course_keys = [uca.course_key for uca in in_process_course_actions]
    courses = [
        course
        for course in courses
        if not isinstance(course, ErrorDescriptor) and (course.id not in in_process_action_course_keys)
    ]

    if request.json:
        course_ids = [str(course.id) for course in courses]
        course_re_run_details = deepcopy(request.json)

        for course in course_re_run_details:
            for re_run in course['runs']:
                start = '{}-{}'.format(re_run['start_date'], re_run['start_time'])
                try:
                    re_run['start'] = datetime.strptime(start, '%m/%d/%Y-%H:%M').replace(tzinfo=utc)
                except ValueError:
                    re_run['error'] = 'Start date/time format is incorrect'
                    course['has_errors'] = True

            if course['source_course_key'] not in course_ids:
                course['error'] = 'Course ID not found'
                course['has_errors'] = True

        # Generate ids

        course_re_run_details = helpers.update_course_re_run_details(course_re_run_details)

        if any([c.get('has_errors', False) for c in course_re_run_details]):
            return JsonResponse(course_re_run_details, status=400)

        # Create courses here

        # Success response here
        return JsonResponse(status=200)

    latest_courses = latest_course_reruns(courses)

    context = {
        'latest_courses': latest_courses
    }

    return render_to_response('rerun/create_multiple_rerun.html', context)
