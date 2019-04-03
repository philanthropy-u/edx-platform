# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


def add_data(apps, schema_editor):
    PartnerNetwork = apps.get_model('onboarding', 'PartnerNetwork')

    last_order = PartnerNetwork.objects.all().order_by('order').last()

    PartnerNetwork.objects.create(
        code="ECHIDNA", label="Echidna Giving", order=last_order.order + 1 if last_order else 1
    )


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('onboarding', '0025_registrationtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='GranteeOptIn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('agreed_at', models.DateTimeField(auto_now_add=True)),
                ('agreed', models.BooleanField()),
                ('organization_partner', models.ForeignKey(related_name='grantee_opt_in', to='onboarding.OrganizationPartner')),
                ('user', models.ForeignKey(related_name='grantee_opt_in', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        # migrations.RunPython(add_data)
    ]
