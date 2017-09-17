"""
Models to support Course Surveys feature
"""

from django.db import models
from student.models import User

from django.db.models import CASCADE, SET_NULL


class OefSurvey(models.Model):
    """
    Model to define an OEF survey
    """
    STATUS_OPTIONS = (
        ('draft', 'draft'),
        ('submitted', 'submitted'),
    )
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=STATUS_OPTIONS, default='draft')
    create_date = models.DateTimeField(auto_now_add=True)
    submit_date = models.DateTimeField(auto_now_add=True, null=True)
    version = models.AutoField(primary_key=True)

    class Meta(object):
        get_latest_by = 'version'

    def __str__(self):
        return 'version_' + str(self.version)


class CategoryPage(models.Model):
    """
    Model to define a category inside a Survey form
    """
    survey = models.ForeignKey(OefSurvey, db_index=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    is_complete = models.BooleanField(default=False)

    class Meta(object):
        unique_together = ('id', 'name', 'survey')
        get_latest_by = 'page_no'

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    survey = models.ForeignKey(OefSurvey, db_index=True, on_delete=CASCADE)
    category = models.ForeignKey(CategoryPage, db_index=True, on_delete=CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)

    class Meta(object):
        unique_together = ('id', 'name', 'category', 'survey')

    def __str__(self):
        return self.name
    

class SurveyQuestion(models.Model):
    survey = models.ForeignKey(OefSurvey, db_index=True, on_delete=CASCADE)
    category = models.ForeignKey(CategoryPage, db_index=True,
        on_delete=CASCADE)
    sub_category = models.ForeignKey(SubCategory, db_index=True,
        null=True, on_delete=SET_NULL)
    statement = models.CharField(max_length=255)
    help_msg = models.CharField(max_length=1000)

    class Meta(object):
        unique_together = ()

    def __str__(self):
        return self.statement


class SurveyQuestionAnswer(models.Model):
    CATEGORY_OPTIONS = (
        ('low', 'Low'),
        ('basic', 'Basic'),
        ('moderate', 'Moderate'),
        ('strong', 'Strong'),
    )
    question = models.ForeignKey(SurveyQuestion, db_index=True, on_delete=CASCADE)
    description = models.CharField(max_length=1000)
    category = models.CharField(max_length=255, choices=CATEGORY_OPTIONS)

    class Meta(object):
        unique_together = ('question', 'category')

class SurveyFeedback(models.Model):
    """
    Model to define an OEF survey Feedback
    """
    user = models.ForeignKey(User, db_index=True, on_delete=CASCADE)
    survey = models.ForeignKey(OefSurvey, db_index=True, null=True,
        on_delete=SET_NULL)
    category = models.ForeignKey(CategoryPage, db_index=True, null=True,
        on_delete=SET_NULL)
    sub_category = models.ForeignKey(SubCategory, db_index=True, null=True,
        on_delete=SET_NULL)
    question = models.ForeignKey(SurveyQuestion, db_index=True, on_delete=CASCADE)
    answer = models.ForeignKey(SurveyQuestionAnswer, db_index=True, on_delete=CASCADE)
