import json
import logging

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from oef_survey.models import UserSurveyFeedback, SurveyFeedback
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


@login_required
@transaction.atomic
def oef_survey_save(request):
    """
    Views to list down all survey added by a user
    """
    # from nose.tools import set_trace; set_trace()
    data = json.loads(request.body)

    feedback = request.GET.get('feedback')

    if feedback:
        user_feedback = UserSurveyFeedback.objects.filter(pk=feedback)
    else:
        user_feedback = UserSurveyFeedback.objects.create(user=request.user, survey_id=data['survey_id'])

    for question, answer in data['questions'].iteritems():
        try:
            survey = SurveyFeedback.objects.get(
                feedback=user_feedback,
                category_id=data['page_id'],
                sub_category_id=data['sub_category_id'],
                question_id=question,
            )
            survey.answer_id = answer
            survey.save()
        except:
            SurveyFeedback.objects.create(
                feedback=user_feedback,
                category_id=data['page_id'],
                sub_category_id=data['sub_category_id'],
                question_id=question,
                answer_id=answer
            )
    return JsonResponse({})
