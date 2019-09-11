# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badging', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badge',
            name='type',
            field=models.CharField(max_length=100, choices=[(b'conversationalist', b'Conversationalist'), (b'team', b'Team player')]),
        ),
    ]
