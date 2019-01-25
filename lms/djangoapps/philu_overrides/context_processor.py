from django.conf import settings

from lms.djangoapps.onboarding.helpers import should_we_show_org_update_prompt
from lms.djangoapps.philu_overrides.constants import ACTIVATION_ERROR, ACTIVATION_ALERT_TYPE, ORG_DETAILS_UPDARE_ALERT


def get_global_alert_messages(request):

    """
    function to get application wide messages
    :param request:
    :return: returns list of global messages"
    """

    alert_messages = []
    if not request.is_ajax():
        if request.user.is_authenticated() and not request.user.is_active and '/activate/' not in request.path:
            alert_messages.append({
                "type": ACTIVATION_ALERT_TYPE,
                "alert": ACTIVATION_ERROR
            })

    if '/organization/details/' in request.path and should_we_show_org_update_prompt(request.user):
        alert_messages.append({
            "type": ACTIVATION_ALERT_TYPE,
            "alert": ORG_DETAILS_UPDARE_ALERT
        })

    return {"alert_messages": alert_messages}


def add_nodebb_endpoint(request):
    """
    Add our NODEBB_ENDPOINT to the template context so that it can be referenced by any client side code.
    """
    return { "nodebb_endpoint": settings.NODEBB_ENDPOINT }
