# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ondemand_email_preferences', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ondemandemailpreferences',
            name='user',
            field=models.ForeignKey(related_name='email_preferences_user', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
    ]
