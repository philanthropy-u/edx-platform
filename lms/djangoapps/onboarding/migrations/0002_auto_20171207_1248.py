# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='city',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='country',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='focus_area',
            field=models.ForeignKey(related_name='organization', to='onboarding.FocusArea', null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='level_of_operation',
            field=models.ForeignKey(related_name='organization', to='onboarding.OperationLevel', null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='org_type',
            field=models.ForeignKey(related_name='organization', to='onboarding.OrgSector', null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='registration_number',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='unclaimed_org_admin_email',
            field=models.EmailField(max_length=254, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='userextendedprofile',
            name='city_of_employment',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userextendedprofile',
            name='country_of_employment',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userextendedprofile',
            name='english_proficiency',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='userextendedprofile',
            name='hours_per_week',
            field=models.PositiveIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(168)]),
        ),
        migrations.AlterField(
            model_name='userextendedprofile',
            name='level_of_education',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='userextendedprofile',
            name='start_month_year',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
