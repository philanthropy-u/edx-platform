"""
Models to support Course Surveys feature
"""

from django.db import models
from django.db.models import CASCADE, SET_NULL
from student.models import User


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
    is_active = models.BooleanField(default=True)

    class Meta(object):
        get_latest_by = 'version'

    def __str__(self):
        return '{}'.format(self.name)


class CategoryPage(models.Model):
    """
    Model to define a category inside a Survey form
    """
    survey = models.ForeignKey(OefSurvey, db_index=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    is_complete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta(object):
        unique_together = ('id', 'name', 'survey')

    def __str__(self):
        return '{} | {}'.format(self.name, self.survey)


class SubCategory(models.Model):
    survey = models.ForeignKey(OefSurvey, db_index=True, on_delete=CASCADE)
    category = models.ForeignKey(CategoryPage, db_index=True, on_delete=CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    is_active = models.BooleanField(default=True)

    class Meta(object):
        unique_together = ('id', 'name', 'category', 'survey')

    def __str__(self):
        return '{} | {} | {}'.format(self.name, self.description, self.category)


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(OefSurvey, db_index=True, on_delete=CASCADE)
    category = models.ForeignKey(CategoryPage, db_index=True, on_delete=CASCADE)
    sub_category = models.ForeignKey(SubCategory, db_index=True, null=True, on_delete=SET_NULL)
    statement = models.CharField(max_length=255)
    help_msg = models.CharField(max_length=1000)
    submit_date = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{} | {} | {}'.format(self.sub_category, self.statement, self.help_msg)


class SurveyQuestionAnswer(models.Model):
    CATEGORY_OPTIONS = (
        ('low', 'Low'),
        ('basic', 'Basic'),
        ('moderate', 'Moderate'),
        ('strong', 'Strong'),
    )

    description = models.CharField(max_length=1000)
    category = models.CharField(max_length=255, choices=CATEGORY_OPTIONS)
    question = models.ForeignKey(SurveyQuestion, db_index=True, on_delete=CASCADE)

    class Meta(object):
        unique_together = ('question', 'category')

    def __str__(self):
        return '{} | {}'.format(self.question, self.description)


class UserSurveyFeedback(models.Model):
    STATUS_OPTIONS = (
        ('incomplete', 'incomplete'),
        ('complete', 'complete'),
    )

    version = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, db_index=True, on_delete=CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True, null=True)
    survey = models.ForeignKey(OefSurvey, db_index=True, null=True, on_delete=SET_NULL)
    status = models.CharField(max_length=255, choices=STATUS_OPTIONS, default='incomplete')

    def __str__(self):
        return '{} | {} | {}'.format(self.user, self.survey, self.version)


class SurveyFeedback(models.Model):
    """
    Model to define an OEF survey Feedback
    """
    feedback = models.ForeignKey(UserSurveyFeedback, db_index=True, on_delete=CASCADE)
    category = models.ForeignKey(CategoryPage, db_index=True, null=True, on_delete=SET_NULL)
    sub_category = models.ForeignKey(SubCategory, db_index=True, null=True, on_delete=SET_NULL)
    question = models.ForeignKey(SurveyQuestion, db_index=True, on_delete=CASCADE)
    answer = models.ForeignKey(SurveyQuestionAnswer, db_index=True, on_delete=CASCADE)

    def __str__(self):
        return '{} | {} | {}'.format(self.feedback, self.question, self.answer)
