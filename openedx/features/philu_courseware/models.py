from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import User

from opaque_keys.edx.django.models import UsageKeyField


class CompetencyAssessmentRecord(TimeStampedModel):

    COMP_ASSESSMENT_TYPES = (
        ('pre', 'Pre Assessment'),
        ('post', 'Post Assesment')
    )

    CORRECTNESS_CHOICES = (
        ('correct', 'Correct'),
        ('incorrect', 'Incorrect'),
    )

    problem_id = UsageKeyField(max_length=255)
    problem_text = models.TextField(null=False)
    assessment_type = models.CharField(max_length=4, choices=COMP_ASSESSMENT_TYPES)

    attempt = models.IntegerField()
    correctness = models.CharField(max_length=9, choices=CORRECTNESS_CHOICES)
    # comma separated choice ids for example 1,2,3
    choice_id = models.CharField(max_length=255)
    choice_text = models.TextField()
    score = models.IntegerField()

    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
