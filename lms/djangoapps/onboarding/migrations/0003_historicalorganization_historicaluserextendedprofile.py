# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import model_utils.fields
import django.db.models.deletion
import lms.djangoapps.onboarding.models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('onboarding', '0002_populate_initial_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalOrganization',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('label', models.CharField(max_length=255, db_index=True)),
                ('country', models.CharField(max_length=255, null=True, blank=True)),
                ('city', models.CharField(max_length=255, null=True, blank=True)),
                ('unclaimed_org_admin_email', models.EmailField(db_index=True, max_length=254, null=True, blank=True)),
                ('url', models.URLField(blank=True, max_length=255, null=True, validators=[lms.djangoapps.onboarding.models.SchemaOrNoSchemaURLValidator])),
                ('founding_year', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('registration_number', models.CharField(max_length=30, null=True, blank=True)),
                ('org_type', models.CharField(max_length=10, null=True, blank=True)),
                ('level_of_operation', models.CharField(max_length=10, null=True, blank=True)),
                ('focus_area', models.CharField(max_length=10, null=True, blank=True)),
                ('total_employees', models.CharField(max_length=10, null=True, blank=True)),
                ('alternate_admin_email', models.EmailField(max_length=254, null=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('admin', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical organization',
            },
        ),
        migrations.CreateModel(
            name='HistoricalUserExtendedProfile',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('country_of_employment', models.CharField(max_length=255, null=True)),
                ('not_listed_gender', models.CharField(max_length=255, null=True, blank=True)),
                ('city_of_employment', models.CharField(max_length=255, null=True)),
                ('english_proficiency', models.CharField(max_length=10, null=True)),
                ('level_of_education', models.CharField(max_length=10, null=True)),
                ('start_month_year', models.CharField(max_length=100, null=True)),
                ('role_in_org', models.CharField(max_length=10, null=True)),
                ('hours_per_week', models.PositiveIntegerField(default=0, verbose_name=b'Typical Number of Hours Worked per Week*', validators=[django.core.validators.MaxValueValidator(168)])),
                ('function_strategy_planning', models.SmallIntegerField(default=0, verbose_name=b'Strategy and planning')),
                ('function_leadership_governance', models.SmallIntegerField(default=0, verbose_name=b'Leadership and governance')),
                ('function_program_design', models.SmallIntegerField(default=0, verbose_name=b'Program design and development')),
                ('function_measurement_eval', models.SmallIntegerField(default=0, verbose_name=b'Measurement, evaluation, and learning')),
                ('function_stakeholder_engagement', models.SmallIntegerField(default=0, verbose_name=b'Stakeholder engagement and partnerships')),
                ('function_human_resource', models.SmallIntegerField(default=0, verbose_name=b'Human resource management')),
                ('function_financial_management', models.SmallIntegerField(default=0, verbose_name=b'Financial management')),
                ('function_fundraising', models.SmallIntegerField(default=0, verbose_name=b'Fundraising and resource mobilization')),
                ('function_marketing_communication', models.SmallIntegerField(default=0, verbose_name=b'Strategy and planning')),
                ('function_system_tools', models.SmallIntegerField(default=0, verbose_name=b'Systems, tools, and processes')),
                ('interest_strategy_planning', models.SmallIntegerField(default=0, verbose_name=b'Strategy and planning')),
                ('interest_leadership_governance', models.SmallIntegerField(default=0, verbose_name=b'Leadership and governance')),
                ('interest_program_design', models.SmallIntegerField(default=0, verbose_name=b'Program design and development')),
                ('interest_measurement_eval', models.SmallIntegerField(default=0, verbose_name=b'Measurement, evaluation, and learning')),
                ('interest_stakeholder_engagement', models.SmallIntegerField(default=0, verbose_name=b'Stakeholder engagement and partnerships')),
                ('interest_human_resource', models.SmallIntegerField(default=0, verbose_name=b'Human resource management')),
                ('interest_financial_management', models.SmallIntegerField(default=0, verbose_name=b'Financial management')),
                ('interest_fundraising', models.SmallIntegerField(default=0, verbose_name=b'Fundraising and resource mobilization')),
                ('interest_marketing_communication', models.SmallIntegerField(default=0, verbose_name=b'Marketing, communications, and PR')),
                ('interest_system_tools', models.SmallIntegerField(default=0, verbose_name=b'Systems, tools, and processes')),
                ('learners_same_region', models.SmallIntegerField(default=0, verbose_name=b'Learners from my region or country')),
                ('learners_similar_oe_interest', models.SmallIntegerField(default=0, verbose_name=b'Learners interested in same areas of organization effectiveness')),
                ('learners_similar_org', models.SmallIntegerField(default=0, verbose_name=b'Learners working for similar organizations')),
                ('learners_diff_who_are_different', models.SmallIntegerField(default=0, verbose_name=b'Learners who are different from me')),
                ('goal_contribute_to_org', models.SmallIntegerField(default=0, verbose_name=b'Help improve my organization')),
                ('goal_gain_new_skill', models.SmallIntegerField(default=0, verbose_name=b'Develop new skills')),
                ('goal_improve_job_prospect', models.SmallIntegerField(default=0, verbose_name=b'Get a job')),
                ('goal_relation_with_other', models.SmallIntegerField(default=0, verbose_name=b'Build relantionships with other nonprofit leaders')),
                ('is_interests_data_submitted', models.BooleanField(default=False)),
                ('is_organization_metrics_submitted', models.BooleanField(default=False)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('organization', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='onboarding.Organization', null=True)),
                ('user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical user extended profile',
            },
        ),
    ]
