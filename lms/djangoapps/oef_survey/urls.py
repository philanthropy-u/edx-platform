"""
URL mappings for the Survey feature
"""

from django.conf.urls import patterns, url
from oef_survey.views import oef_survey

urlpatterns = [
	url(r'$', oef_survey, name='oef_survey'),
]
