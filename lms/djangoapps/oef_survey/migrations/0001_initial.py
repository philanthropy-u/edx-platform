# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
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
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1000)),
                ('is_complete', models.BooleanField(default=False)),
            ],
            options={
                'get_latest_by': 'page_no',
            },
        ),
        migrations.CreateModel(
            name='OefSurvey',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(default=b'draft', max_length=255, choices=[(b'draft', b'draft'), (b'submitted', b'submitted')])),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('submit_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('version', models.AutoField(serialize=False, primary_key=True)),
            ],
            options={
                'get_latest_by': 'version',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1000)),
                ('category', models.ForeignKey(to='oef_survey.CategoryPage')),
                ('survey', models.ForeignKey(to='oef_survey.OefSurvey')),
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
                ('statement', models.CharField(max_length=255)),
                ('help_msg', models.CharField(max_length=1000)),
                ('category', models.ForeignKey(to='oef_survey.CategoryPage')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='oef_survey.SubCategory', null=True)),
                ('survey', models.ForeignKey(to='oef_survey.OefSurvey')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyQuestionAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=1000)),
                ('category', models.CharField(max_length=255, choices=[(b'low', b'Low'), (b'basic', b'Basic'), (b'moderate', b'Moderate'), (b'strong', b'Strong')])),
                ('question', models.ForeignKey(to='oef_survey.SurveyQuestion')),
            ],
        ),
        migrations.AddField(
            model_name='surveyfeedback',
            name='answer',
            field=models.ForeignKey(to='oef_survey.SurveyQuestionAnswer'),
        ),
        migrations.AddField(
            model_name='surveyfeedback',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='oef_survey.CategoryPage', null=True),
        ),
        migrations.AddField(
            model_name='surveyfeedback',
            name='question',
            field=models.ForeignKey(to='oef_survey.SurveyQuestion'),
        ),
        migrations.AddField(
            model_name='surveyfeedback',
            name='sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='oef_survey.SubCategory', null=True),
        ),
        migrations.AddField(
            model_name='surveyfeedback',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='oef_survey.OefSurvey', null=True),
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
        migrations.AlterUniqueTogether(
            name='subcategory',
            unique_together=set([('id', 'name', 'category', 'survey')]),
        ),
        migrations.AlterUniqueTogether(
            name='categorypage',
            unique_together=set([('id', 'name', 'survey')]),
        ),
    ]
