"""Defines the URL routes for this app."""

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import my_team, browse_teams

urlpatterns = patterns(
    'openedx.features.teams.views',
    url(r"^my_team/$", login_required(my_team), name="my_team"),
    url(r"^browse_teams/$", login_required(browse_teams), name="browse_teams")
)
