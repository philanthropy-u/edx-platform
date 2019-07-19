"""
Views for on-demand-email-preferences app.
"""
import logging
from django.http import JsonResponse
from opaque_keys.edx.keys import CourseKey
from openedx.features.ondemand_email_preferences.models import OnDemandEmailPreferences
from django.views.decorators.csrf import csrf_exempt

log = logging.getLogger("edx.ondemand_email_preferences")


@csrf_exempt
def update_on_demand_emails_preferences_component(request, course_id, *args, **kwargs):
    """
    Used to fetch the email preferences of self paced course
    :param request:
    :course_id: Course id of Self paced Course
    :return:
    {
        "status": "200",
        "email_preferences": "boolean"
    }
    """

    try:
        email_preferences = OnDemandEmailPreferences.objects.get(user=request.user,
                                                                 course_id=CourseKey.from_string(course_id))
        return JsonResponse({'status': 200, 'email_preferences': email_preferences.is_enabled})

    except OnDemandEmailPreferences.DoesNotExist:
        return JsonResponse({'status': 200, 'email_preferences': True})
