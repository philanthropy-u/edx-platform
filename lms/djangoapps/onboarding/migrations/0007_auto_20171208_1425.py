# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0006_auto_20171208_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextendedprofile',
            name='role_in_org',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
