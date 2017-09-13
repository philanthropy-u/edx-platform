"""
URL mappings for the Survey feature
"""

from django.conf.urls import patterns, url


urlpatterns = patterns(
    'global_survey.views',

    url(r'^oef_survey$', 'view_survey', name='view_survey'),
)
