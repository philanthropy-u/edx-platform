# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2021-01-19 14:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job_board', '0005_auto_20200504_0545'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='job_post', related_query_name='job_post', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
