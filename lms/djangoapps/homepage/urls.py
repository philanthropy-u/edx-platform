from django.conf.urls import url
from lms.djangoapps.homepage.views import *

urlpatterns = [
    url(r'', home_page, name='homepage'),
]