"""Defines the URL routes for this app."""

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import browse_teams, create_team, my_team

urlpatterns = patterns(
    'openedx.features.teams.views',

    url(r"^browse_teams/$", login_required(browse_teams), name="browse_teams"),
    url(r"^(?P<region>[a-z0-9]+)/create/$", login_required(create_team), name="create_team"),
    url(r"^my_team/$", login_required(my_team), name="my_team"),
)
