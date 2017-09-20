# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('oef_survey', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categorypage',
            options={},
        ),
        migrations.AddField(
            model_name='oefsurvey',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='surveyquestion',
            name='submit_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='usersurveyfeedback',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 15, 22, 12, 39, 462216, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='usersurveyfeedback',
            name='submitted_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
