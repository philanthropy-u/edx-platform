from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel


class ThirdPartySurvey(TimeStampedModel):
    """
    Model that stores third party surveys
    """
    response = models.TextField()
    request_date = models.CharField(max_length=19)
    user = models.ForeignKey(User, related_name='survey_user')
    type = models.CharField(max_length=20, null=True, blank=True)

    def __unicode__(self):
        return "{} | {} | {}".format(self.user, self.type, self.request_date)
