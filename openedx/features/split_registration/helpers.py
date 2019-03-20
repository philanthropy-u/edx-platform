from ipware.ip import get_ip
from opaque_keys import InvalidKeyError

from django.core.urlresolvers import reverse

from xmodule.modulestore.django import modulestore
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from openedx.core.djangoapps.embargo import api as embargo_api
from student.models import CourseEnrollment


def enroll_in_course(request, action, course_id):
    try:
        course_id = SlashSeparatedCourseKey.from_deprecated_string(course_id)
    except InvalidKeyError:
        return False

    if action == "enroll":
        user = request.user
        # Make sure the course exists
        # We don't do this check on unenroll, or a bad course id can't be unenrolled from
        if not modulestore().has_course(course_id):
            return False

        # Check whether the user is blocked from enrolling in this course
        # This can occur if the user's IP is on a global blacklist
        # or if the user is enrolling in a country in which the course
        # is not available.
        redirect_url = embargo_api.redirect_if_blocked(
            course_id, user=user, ip_address=get_ip(request),
            url=request.path
        )
        if redirect_url:
            return redirect_url

        try:
            CourseEnrollment.enroll(user, course_id, check_access=True)
        except Exception as e:  # pylint: disable=broad-except
            return False

        course_target = reverse('about_course', args=[unicode(course_id)])

        return course_target
