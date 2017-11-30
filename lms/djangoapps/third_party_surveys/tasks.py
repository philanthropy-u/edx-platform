
from surveygizmo import SurveyGizmo
from lms.djangoapps.third_party_surveys.models import ThirdPartySurvey
from datetime import date, timedelta
from celery.task import periodic_task
from celery.schedules import crontab
import json

@periodic_task(run_every=crontab())
def get_third_party_surveys():
    survey_client = SurveyGizmo(
        api_version='v4',
        api_token = "",
        api_token_secret = ""
    )

    surveys = survey_client.api.survey.list()
    last_survey = ThirdPartySurvey.objects.last()
    last_requested_date = date.today() - timedelta(1)

    print(len(surveys['data']))

    if last_survey:
        last_requested_date = last_survey.request_date

    for survey in surveys['data']:
        print(str(last_requested_date))
        print(str(date.today()))
        survey_response = survey_client.api.surveyresponse\
            .filter('datesubmitted','>=', str(last_requested_date))\
            .filter('datesubmitted','<', str(date.today()))\
            .list(survey['id'])

        print(survey_response['data'])

        third_party_survey = ThirdPartySurvey(response=json.dumps(survey_response['data']), request_date=date.today())
        third_party_survey.save()