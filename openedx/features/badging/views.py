from django.views.decorators.http import require_GET
from django.http import Http404
# from util.json_request import JsonResponse
from edxmako.shortcuts import render_to_response
from student.models import CourseEnrollment, AnonymousUserId

from .helpers import populate_trophycase
from .models import UserBadge


@require_GET
def trophy_case(request):
    # Get course id and course name of courses user is enrolled in

    # try:
    #     user = AnonymousUserId.objects.get(anonymous_user_id=uuid).user
    # except AnonymousUserId.DoesNotExist:
    #     raise Http404()
    #
    # enrolled_courses_data = CourseEnrollment.enrollments_for_user(user).order_by(
    #     'course__display_name').values_list('course_id', 'course__display_name')
    #
    # # list of badges earned by user
    # earned_user_badges = list(
    #     UserBadge.objects.filter(user=user)
    # )
    #
    # trophycase_dict = populate_trophycase(enrolled_courses_data, earned_user_badges)

    # return JsonResponse(trophycase_dict)

    return render_to_response(
        "features/badging/trophy_case.html",
        {
            'course_badges': []
        }
    )
