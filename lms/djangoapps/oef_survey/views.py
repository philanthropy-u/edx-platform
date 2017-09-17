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
    user = request.user
    user_profile = user.profile

    # Context dictionary for template rendering
    context = dict()

    # If user is not POC hide this view from user
    if not user_profile.is_poc:
        return page_not_found(request)

    # If there are multiple versions of the OEF survey always
    # return the latest one
    # TODO: if no servey exists redirect or show error message
    servey = OefSurvey.objects.latest()

    if not survey:
        return page_not_found(request)

    context.update({"survey_name": survey.name,
        "survey_created": survey.create_date,
    })

    # Get the first incomplete Cagtegory Page
    # If all pages are complete get the last one
    # TODO: if survey has no pages redirect or show error message
    page = CategoryPage.objects.filter(is_complete=False).earliest()

    if not page:
        page = CategoryPage.objects.latest()

    context.update({"page_title": page.name,
        "page_desc": page.description,
        "page_no": page.page_no,
    })

    # Get Sub-Categories for current page
    # TODO: handle case if page has no contect
    sub_categories = SubCategory.objects.filter(category=page)

    for sub_category in sub_categories:
        sub_categories_dict = {"sub_category_title": sub_category.name,
            "sub_category_desc": sub_category.description,
        }

        questions = SurveyQuestion.objects.filter(survey=survey,
            category=page,
            sub_category=sub_category)
        questions_list = []

        for question in questions:
            options = SurveyQuestionAnswer.objects.filter(question=question)
            answer_dict = {"statement": question.statement}

            for option in options:
                answer_dict.update({options.category: options.description})

            questions_list.append(answer_dict)

        sub_categories_dict.update({"questions": questions_list})

    context.update({"sub_categories": sub_categories_dict})

    from nose.tools import set_trace; set_trace();
    return page_not_found(request)


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