# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-10 17:15
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identity', models.CharField(max_length=2048, unique=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_update', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=512)),
                ('body', models.TextField()),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
                ('read', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
