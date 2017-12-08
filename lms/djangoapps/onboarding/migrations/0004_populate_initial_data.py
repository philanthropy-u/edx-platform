# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    def insert_education_levels(apps, schema_editor):
         
        _levels = {
            "DPD": "Doctoral or professional degree",
            "MD": "Master's degree",
            "BD": "Bachelor's degree",
            "AD": "Associate's degree",
            "PNA": "Postsecondary nondegree award",
            "SCND": "Some college, no degree",
            "HSDOE": "High school diploma or equivalent",
            "NFE": "No formal educational credential"
        }
        EducationLevel = apps.get_model('onboarding', 'EducationLevel')

        objs = []
        for code, label in _levels.items():
            objs.append(EducationLevel(code=code, label=label))

        EducationLevel.objects.bulk_create(objs)

    def insert_english_proficiency(apps, schema_editor):
        _levels = {
            "NP": "No proficiency",
            "EP": "Elementary proficiency",
            "LWP": "Limited working proficiency",
            "PWP": "Professional working proficiency",
            "NOBP": "Native or bilingual proficiency"
        }
        EnglishProficiency = apps.get_model('onboarding', 'EnglishProficiency')

        objs = []
        for code, label in _levels.items():
            objs.append(EnglishProficiency(code=code, label=label))

        EnglishProficiency.objects.bulk_create(objs)

    def insert_role_inside_org(apps, schema_editor):
        _levels = {
            "VOL": "Volunteer",
            "EL": "Entry level",
            "ASSO": "Associate",
            "INTERN": "Internship",
            "MSL": "Mid-Senior level",
            "DIR": "Director",
            "EXC": "Executive",
        }
        RoleInsideOrg = apps.get_model('onboarding', 'RoleInsideOrg')

        objs = []
        for code, label in _levels.items():
            objs.append(RoleInsideOrg(code=code, label=label))

        RoleInsideOrg.objects.bulk_create(objs)

    dependencies = [
        ('onboarding', '0003_auto_20171208_0652'),
    ]

    operations = [
        migrations.RunPython(insert_education_levels),
        migrations.RunPython(insert_english_proficiency),
        migrations.RunPython(insert_role_inside_org),
    ]
