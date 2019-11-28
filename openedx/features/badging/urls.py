from django.conf.urls import url

from .views import trophy_case

urlpatterns = [
    url(r'^trophycase/$', trophy_case, name='trophycase'),
]
