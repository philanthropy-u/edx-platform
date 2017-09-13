"""
Views for OEF Surveys
"""
import json

from django.contrib.auth.decorators import login_required
from edxmako.shortcuts import render_to_response, render_to_string
from django.http import (HttpResponse, HttpResponseServerError,
                         HttpResponseNotFound)
from onboarding_survey.models import GlobalSurvey


logger = logging.getLogger(__name__)


def page_not_found(request):
    return HttpResponseNotFound(render_to_string('404.html', {}, request=request))


@login_required
def view_survey(request):
    """
    Views to render each page of OEF Survey
    """
    ser = request.user
    user_profile = request.user.user_profile

    # If user is not POC hide this view from user
    if not user_profile.is_poc:
        return page_not_found(request)

    return page_not_found(request)

    


@require_POST
@login_required
def submit_answer(request):
    """
    User feedback REST API
    """
    user = request.user
    user_profile = request.user.user_profile