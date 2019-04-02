# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def add_data(apps, schema_editor):
    PartnerNetwork = apps.get_model('onboarding', 'PartnerNetwork')

    last_order = PartnerNetwork.objects.all().order_by('order').last()

    PartnerNetwork.objects.create(
        code="ECHIDNA", label="Echidna Giving", order=last_order.order + 1 if last_order else 1
    )


class Migration(migrations.Migration):
    dependencies = [
        ('onboarding', '0025_registrationtype'),
    ]

    operations = [
        migrations.RunPython(add_data)
    ]
