# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-02-28 09:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openstack_tenant', '0020_remove_external_ips'),
    ]

    operations = [
        migrations.AddField(
            model_name='instance',
            name='subnets',
            field=models.ManyToManyField(through='openstack_tenant.InternalIP', to='openstack_tenant.SubNet'),
        ),
    ]
