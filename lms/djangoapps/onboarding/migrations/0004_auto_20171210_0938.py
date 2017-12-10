# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0003_auto_20171210_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationmetric',
            name='local_currency',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
