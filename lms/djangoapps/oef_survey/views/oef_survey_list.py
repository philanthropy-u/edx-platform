import logging

from django.contrib.auth.decorators import login_required
from oef_survey.models import UserSurveyFeedback
from edxmako.shortcuts import render_to_response
from datetime import datetime, timedelta
from django.utils import timezone

logger = logging.getLogger(__name__)


@login_required
def oef_survey_list(request):
    """
    Views to list down all survey added by a user
    """
    surveys = UserSurveyFeedback.objects.filter(user_id=request.user)

    # if current date is less then expiry date
    button_enabled = True
    if surveys and surveys.latest('version').created_at + timedelta(days=6*30) > datetime.now(timezone.utc):
        button_enabled = False

    context = {'surveys': surveys, 'button_enabled': button_enabled}
    return render_to_response("oef_survey/oef_survey_list.html", context)
