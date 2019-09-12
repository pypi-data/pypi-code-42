# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-10-30 06:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bee_django_user', '0009_userleavestatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='userleaverecord',
            name='info',
            field=models.TextField(blank=True, null=True, verbose_name='\u5907\u6ce8'),
        ),
        migrations.AlterField(
            model_name='userleaverecord',
            name='type',
            field=models.IntegerField(choices=[(1, '\u8bf7\u5047'), (2, '\u9500\u5047'), (3, '\u5ef6\u671f/\u63d0\u524d')], default=1, verbose_name='\u7c7b\u578b'),
        ),
    ]
