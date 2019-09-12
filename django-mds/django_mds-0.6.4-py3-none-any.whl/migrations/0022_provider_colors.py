# Generated by Django 2.1.7 on 2019-05-17 13:48

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("mds", "0021_rename_event_source")]

    operations = [
        migrations.AddField(
            model_name="provider",
            name="colors",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                blank=True,
                default=dict,
                verbose_name="colors for distinguishing provider icons",
            ),
        )
    ]
