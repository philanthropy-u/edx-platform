# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oef_survey', '0004_usersurveyfeedback_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorypage',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='surveyquestion',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
