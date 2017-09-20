"""
URL mappings for the Survey feature
"""

from django.conf.urls import url
from lms.djangoapps.oef_survey.views.oef_survey_list import oef_survey_list
from lms.djangoapps.oef_survey.views.oef_survey_detail import oef_survey_detail
from lms.djangoapps.oef_survey.views.oef_survey_save import oef_survey_save

urlpatterns = [
    url(r'^list', oef_survey_list, name='oef_survey_list'),
    url(r'^save', oef_survey_save, name='oef_survey_save'),
    url(r'$', oef_survey_detail, name='oef_survey'),
]
