# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oef_survey', '0003_auto_20170915_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersurveyfeedback',
            name='status',
            field=models.CharField(default=b'incomplete', max_length=255, choices=[(b'incomplete', b'incomplete'), (b'complete', b'complete')]),
        ),
    ]
