# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-08-30 06:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bee_django_report', '0004_auto_20190711_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='classweek',
            name='live_commented_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='classweek',
            name='live_watched_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='classweek',
            name='live_watched_days',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='classweek',
            name='feed_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='classweek',
            name='live_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='classweek',
            name='live_days',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='classweek',
            name='live_mins',
            field=models.IntegerField(default=0),
        ),
    ]
