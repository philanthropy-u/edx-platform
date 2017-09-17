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
    from nose.tools import set_trace; set_trace()
    user = request.user
    user_profile = user.profile
    requested_page = request.GET.get('page', None)


    # Context dictionary for template rendering
    context = dict()

    # If user is not POC hide this view from user
    # if not user_profile.is_poc:
    #     return page_not_found(request)

    # If there are multiple versions of the OEF survey always
    # return the latest one
    # TODO: if no servey exists redirect or show error message
    survey = OefSurvey.objects.latest()

    if not survey:
        return page_not_found(request)

    context.update({"survey_name": survey.name,
        "survey_created": survey.create_date,
    })

    
    complete_pages = CategoryPage.objects.filter(is_complete=True).count()
    incomplete_pages = CategoryPage.objects.filter(is_complete=False).count()
    total_pages = complete_pages + incomplete_pages
    # Get the first incomplete Cagtegory Page
    # If all pages are complete get the last one
    # TODO: if survey has no pages redirect or show error message
    if not requested_page:
        page = CategoryPage.objects.filter(is_complete=False).first()
        page_no = 0
    else:
        try:
            page_no = int(requested_page)
            pages = CategoryPage.objects.all()
            page = pages[page_no]
        except TypeError:
            return page_not_found(request)

    if not page:
        page = CategoryPage.objects.last()
        page_no = total_pages - 1

    context.update({"page_title": page.name,
        "page_desc": page.description,
        "page_no": page_no,
        "total_pages": total_pages,
        "complete_pages": complete_pages,
        "incomplete_pages": incomplete_pages
    })

    # Get Sub-Categories for current page
    # TODO: handle case if page has no contect
    sub_categories = SubCategory.objects.filter(category=page)
    sub_categories_list = []

    for sub_category in sub_categories:
        questions = SurveyQuestion.objects.filter(survey=survey,
            category=page,
            sub_category=sub_category)
        questions_list = []

        for question in questions:
            options = SurveyQuestionAnswer.objects.filter(question=question)
            question_dict = {"statement": question.statement}

            for option in options:
                question_dict.update({option.category: option.description})

            questions_list.append(question_dict)

        sub_categories_list.append({"sub_category_title": sub_category.name,
            "sub_category_desc": sub_category.description,
            "questions": questions_list
        })

    context.update({"sub_categories": sub_categories_list})
    return render_to_response("oef_survey/oef_page.html", context)


@login_required
def submit_answer(request):
    """
    User feedback REST API
    """
    return page_not_found(request)