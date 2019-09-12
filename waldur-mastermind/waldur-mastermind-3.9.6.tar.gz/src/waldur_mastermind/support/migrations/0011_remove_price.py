# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-14 00:19
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_offering_price(apps, schema_editor):
    Offering = apps.get_model('support', 'Offering')
    for offering in Offering.objects.all():
        offering.unit_price = offering.price
        offering.save(update_fields=['unit_price'])


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0010_add_unit_price'),
    ]

    operations = [
        migrations.RunPython(migrate_offering_price, elidable=True),
        migrations.RemoveField(
            model_name='offering',
            name='price',
        ),
    ]
