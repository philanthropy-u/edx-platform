"""Defines the URL routes for this app."""

from django.conf.urls import patterns, url

from .views import browse_teams, create_team, my_team, browse_topic_teams, update_team, view_team

urlpatterns = patterns(
    'openedx.features.teams.views',

    url(r"^browse_teams/$", browse_teams, name="browse_teams"),
    url(r"^browse_teams/(?P<topic_id>[A-Za-z0-9]+)/$", browse_topic_teams, name="browse_topic_teams"),
    url(r"^(?P<topic_id>[A-Za-z0-9]+)/create/$", create_team, name="create_team"),
    url(r"^(?P<team_id>[a-z\d_-]+)/update/$", update_team, name="update_team"),
    url(r"^my_team/$", my_team, name="my_team"),
    url(r"^team/(?P<team_id>[A-Za-z0-9]+)$", view_team, name="view_team"),
)
