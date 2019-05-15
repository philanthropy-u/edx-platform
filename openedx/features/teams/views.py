from django.shortcuts import render_to_response

from opaque_keys.edx.keys import CourseKey
from courseware.courses import get_course_with_access


def my_team(request, course_id):
        course_key = CourseKey.from_string(course_id)
        course = get_course_with_access(request.user, "load", course_key)

        context = {
            'course': course,
        }

        return render_to_response("teams/my_team.html", context)


def browse_teams(request, course_id):
    course_key = CourseKey.from_string(course_id)
    course = get_course_with_access(request.user, "load", course_key)

    context = {
        'course': course,
    }

    return render_to_response("teams/browse_teams.html", context)

