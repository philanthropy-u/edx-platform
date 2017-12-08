# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0004_populate_initial_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextendedprofile',
            name='hours_per_week',
            field=models.PositiveIntegerField(null=True, verbose_name=b'Typical Number of Hours Worked per Week', validators=[django.core.validators.MaxValueValidator(168)]),
        ),
        migrations.AlterField(
            model_name='userextendedprofile',
            name='not_listed_gender',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
