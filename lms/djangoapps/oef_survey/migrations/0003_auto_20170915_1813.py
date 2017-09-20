# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oef_survey', '0002_auto_20170915_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersurveyfeedback',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
