"""
Urls for smart_referral app
"""
from django.conf.urls import url

from openedx.features.smart_referral.api_views import FilterContactsAPIView, send_initial_emails_and_save_record

urlpatterns = [
    url(r'^initial_emails/$', send_initial_emails_and_save_record, name='initial_referral_emails'),
    url(
        r'^api/filter_contacts/$',
        FilterContactsAPIView.as_view(),
        name='filter_user_contacts'
    )
]
