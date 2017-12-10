# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0002_populate_initial_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalorganization',
            name='city',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalorganization',
            name='country',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalorganization',
            name='focus_area',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalorganization',
            name='level_of_operation',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalorganization',
            name='org_type',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalorganization',
            name='registration_number',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalorganization',
            name='total_employees',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalorganization',
            name='unclaimed_org_admin_email',
            field=models.EmailField(db_index=True, max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='city',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='country',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='focus_area',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='level_of_operation',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='org_type',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='registration_number',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='total_employees',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='unclaimed_org_admin_email',
            field=models.EmailField(max_length=254, unique=True, null=True, blank=True),
        ),
        migrations.RemoveField(
            model_name='organizationpartner',
            name='partner',
        ),
        migrations.AddField(
            model_name='organizationpartner',
            name='partner',
            field=models.ForeignKey(related_name='organization_partners', default=1, to='onboarding.PartnerNetwork'),
            preserve_default=False,
        ),
    ]
