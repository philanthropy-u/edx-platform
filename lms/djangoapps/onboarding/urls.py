"""
The urls for on-boarding app.
"""
from django.conf.urls import patterns, url

from onboarding import views


urlpatterns = [
    url(r"^onboarding/recommendations/$", views.recommendations, name="recommendations"),
    url(r"^onboarding/user_info/$", views.user_info, name="user_info"),  # signup step 1
    url(r"^onboarding/interests/$", views.interests, name="interests"),  # signup step 2
    url(r"^onboarding/organization/$", views.organization, name="organization"),  # signup step 3
    url(r"^onboarding/get_country_names/$", views.get_country_names, name="get_country_names"),
    url(r"^onboarding/get_languages/$", views.get_languages, name="get_languages"),
    url(r"^myaccount/settings/$", views.update_account_settings, name="update_account_settings"),
    url(r"^onboarding/get_user_organizations/$", views.get_user_organizations, name="get_user_organizations"),
    url(r"^onboarding/get_currencies/$", views.get_currencies, name="get_currencies"),
    url(r"^onboarding/organization_detail/$", views.org_detail_survey, name="org_detail_survey"), # signup step 4
    url(r"^onboarding/delete_account/$", views.delete_my_account, name="delete_my_account"), # signup step 4
    url(r"^onboarding/admin_activate/(?P<org_id>[^/]*)/(?P<activation_key>[^/]*)$", views.admin_activation, name="admin_activation"),
]
