# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0002_auto_20171207_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextendedprofile',
            name='not_listed_gender',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userextendedprofile',
            name='function_marketing_communication',
            field=models.SmallIntegerField(default=0, verbose_name=b'Strategy and planning'),
        ),
    ]
