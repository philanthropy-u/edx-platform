# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('description', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='OefSurvey',
            fields=[
                ('name', models.CharField(max_length=255, db_index=True)),
                ('status', models.CharField(max_length=255, choices=[(b'draft', b'draft'), (b'submitted', b'submitted')])),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('submit_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('version', models.AutoField(serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, db_index=True)),
                ('description', models.CharField(max_length=1000)),
                ('category', models.ForeignKey(to='oef_survey.CategoryPage')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyFeedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('help_msg', models.CharField(max_length=1000)),
                ('sub_category', models.ForeignKey(to='oef_survey.SubCategory')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyQuestionAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=1000)),
                ('category', models.CharField(max_length=255, choices=[(1, b'Low'), (2, b'Basic'), (3, b'Moderate'), (4, b'Strong')])),
                ('question', models.ForeignKey(to='oef_survey.SurveyQuestion')),
            ],
        ),
        migrations.AddField(
            model_name='surveyfeedback',
            name='answer',
            field=models.ForeignKey(to='oef_survey.SurveyQuestionAnswer', null=True),
        ),
        migrations.AddField(
            model_name='surveyfeedback',
            name='question',
            field=models.ForeignKey(to='oef_survey.SurveyQuestion', null=True),
        ),
        migrations.AddField(
            model_name='surveyfeedback',
            name='survey',
            field=models.ForeignKey(to='oef_survey.OefSurvey'),
        ),
        migrations.AddField(
            model_name='surveyfeedback',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='categorypage',
            name='survey',
            field=models.ForeignKey(to='oef_survey.OefSurvey'),
        ),
        migrations.AlterUniqueTogether(
            name='surveyquestionanswer',
            unique_together=set([('question', 'category')]),
        ),
    ]
