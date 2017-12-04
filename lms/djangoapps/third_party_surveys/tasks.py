from celery.schedules import crontab
from celery.task import periodic_task
from django.conf import settings
from surveygizmo import SurveyGizmo
from django.contrib.auth.models import User

from lms.djangoapps.third_party_surveys.models import ThirdPartySurvey


@periodic_task(run_every=crontab())
def get_third_party_surveys():
    """
    Periodic Task that will run on daily basis and will sync the response data
    of all surveys thorough Survey Gizmo APIs
    """
    survey_client = SurveyGizmo(
        api_version='v4',
        api_token=settings.SURVEY_GIZMO_TOKEN,
        api_token_secret=settings.SURVEY_GIZMO_TOKEN_SECRET
    )

    surveys = survey_client.api.survey.list()
    try:
        last_survey = ThirdPartySurvey.objects.latest('request_date')
    except ThirdPartySurvey.DoesNotExist:
        last_survey = ''

    for survey in surveys['data']:
        survey_response_filter = survey_client.api.surveyresponse
        if last_survey:
            # Increased the page size to decrease the no of requests hitting on Survey Gizmo servers
            survey_response_filter = survey_response_filter.resultsperpage('500').filter(
                'datesubmitted', '>', last_survey.request_date
            )

        survey_responses = survey_response_filter.list(survey['id'])

        # Pagination
        total_pages = survey_responses['total_pages']

        for page in range(survey_responses['page'] + 1, total_pages + 1):
            survey_page_responses = survey_response_filter.page(page).list(survey['id'])
            save_responses(survey_page_responses['data'])

        save_responses(survey_responses['data'])


def save_responses(survey_responses):
    for response in survey_responses:
        if not response.get('[url("sguid")]'):
            continue

        third_party_survey = ThirdPartySurvey(
            response=response,
            user_id=response['[url("sguid")]'],
            request_date=response['datesubmitted']
        )
        third_party_survey.save()
