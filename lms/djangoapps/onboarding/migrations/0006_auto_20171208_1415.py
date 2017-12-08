# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0005_auto_20171208_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextendedprofile',
            name='hours_per_week',
            field=models.PositiveIntegerField(default=0, verbose_name=b'Typical Number of Hours Worked per Week', validators=[django.core.validators.MaxValueValidator(168)]),
            preserve_default=False,
        ),
    ]
