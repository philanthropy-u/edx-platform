# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import openedx.core.djangoapps.xmodule_django.models


class Migration(migrations.Migration):

    dependencies = [
        ('ondemand_email_preferences', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ondemandemailpreferences',
            name='course_id',
            field=openedx.core.djangoapps.xmodule_django.models.CourseKeyField(max_length=255, db_index=True),
        ),
    ]
