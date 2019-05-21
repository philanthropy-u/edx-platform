"""Defines the URL routes for this app."""

from django.conf.urls import patterns, url

from .views import browse_teams, create_team, my_team, browse_topic_teams

urlpatterns = patterns(
    'openedx.features.teams.views',

    url(r"^browse_teams/$", browse_teams, name="browse_teams"),
    url(r"^browse_teams/(?P<topic_id>[A-Za-z0-9]+)/$", browse_topic_teams, name="browse_topic_teams"),
    url(r"^(?P<topic_id>[A-Za-z0-9]+)/create/$", create_team, name="create_team"),
    url(r"^my_team/$", my_team, name="my_team"),
)
