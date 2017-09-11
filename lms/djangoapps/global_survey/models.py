"""
Models to support Course Surveys feature
"""

from django.db import models
from student.models import User


class GlobalSurvey(models.Model):
    """
    Model to define an OEF survey
    """
    STATUS_OPTIONS = (
        ('draft', 'draft'),
        ('submitted', 'submitted'),
    )
    name = models.CharField(max_length=255, db_index=True, unique=True)
    status = models.CharField(max_length=255, choices=STATUS_OPTIONS)
    create_date = models.DateTimeField(auto_now_add=True)
    submit_date = models.DateTimeField(auto_now_add=True, null=True)


class Catogery(models.Model):
    """
    Model to define a category inside a Survey form
    """
    survey = models.ForeignKey(GlobalSurvey, db_index=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=1000)


class SubCategory(models.Model):
    category = models.ForeignKey(Catogery, db_index=True)
    name = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=1000)
    

class SurveyQuestion(models.Model):
    name = models.CharField(max_length=255)
    help_msg = models.CharField(max_length=255, db_index=True)


class SurveyQuestionAnswer(models.Model):
    CATEGORY_OPTIONS = (
        (1, 'Low'),
        (2, 'Basic'),
        (3, 'Moderate'),
        (4, 'Strong'),
    )
    question = models.ForeignKey(SurveyQuestion, db_index=True)
    description = models.CharField(max_length=1000)
    category = models.CharField(max_length=255, choices=CATEGORY_OPTIONS)

    class Meta(object):
        unique_together = ('question', 'category')


class GlobalSurveyUserFeedback(models.Model):
    """
    Model to define an OEF survey
    """
    survey = models.ForeignKey(GlobalSurvey, db_index=True)
    user = models.ForeignKey(User, db_index=True)

class GlobalSurveyFeedback(models.Model):
    question = models.ForeignKey(SurveyQuestion, db_index=True)
    answer = models.ForeignKey(SurveyQuestionAnswer, db_index=True)
