from django.db import models


class ThirdPartySurvey(models.Model):
    """
    Model that stores third party surveys
    """
    response = models.TextField()
    request_date = models.DateField()
