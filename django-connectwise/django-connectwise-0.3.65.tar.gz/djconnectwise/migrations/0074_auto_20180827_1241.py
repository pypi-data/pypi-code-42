# Generated by Django 2.0 on 2018-08-27 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djconnectwise', '0073_auto_20180824_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slapriority',
            name='plan_within',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='slapriority',
            name='resolution_hours',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='slapriority',
            name='respond_hours',
            field=models.FloatField(),
        ),
    ]
