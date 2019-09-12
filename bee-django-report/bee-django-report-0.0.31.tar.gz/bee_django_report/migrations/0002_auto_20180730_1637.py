# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-07-30 08:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bee_django_report', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MentorScoreWeek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(verbose_name='\u5e74')),
                ('week', models.IntegerField(null=True, verbose_name='\u7b2c\u51e0\u5468')),
                ('score', models.FloatField(null=True, verbose_name='\u5206\u6570')),
                ('rank', models.IntegerField(null=True)),
                ('level', models.IntegerField(null=True)),
                ('info', models.TextField(blank=True, null=True, verbose_name='\u5907\u6ce8')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('mentor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
                'db_table': 'bee_django_report_montor_score_week',
            },
        ),
        migrations.RemoveField(
            model_name='mentorscore',
            name='mentor',
        ),
        migrations.DeleteModel(
            name='mentorScore',
        ),
    ]
