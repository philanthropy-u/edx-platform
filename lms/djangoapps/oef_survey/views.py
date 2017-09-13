"""
Views for OEF Surveys
"""
import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import (HttpResponse, HttpResponseServerError,
    HttpResponseNotFound)
from django.views.decorators.http import require_http_methods


from edxmako.shortcuts import render_to_response, render_to_string

from oef_survey.models import (OefSurvey, CategoryPage, SubCategory,
    SurveyQuestion, SurveyQuestionAnswer, SurveyFeedback)

logger = logging.getLogger(__name__)

def page_not_found(request):
    return HttpResponseNotFound(render_to_string('static_templates/404.html', {}, request=request))


@login_required
def oef_survey(request):
    """
    Views to render each page of OEF Survey
    """
    from nose.tools import set_trace; set_trace();
    user = request.user
    user_profile = user.profile

    # If user is not POC hide this view from user
    if not user_profile.is_poc:
        return page_not_found(request)


    
    return render_to_response('static_templates/404.html')

    


@login_required
def submit_answer(request):
    """
    User feedback REST API
    """
    from nose.tools import set_trace; set_trace();
    user = request.user
    user_profile = user.user_profile

    # If user is not POC hide this view from user
    if not user_profile.is_poc:
        return page_not_found(request)



    return page_not_found(request)