from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^automate-rerun/$", views.automate_rerun, name="automate_rerun"),
]
