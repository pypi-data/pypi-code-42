# Generated by Django 2.2.4 on 2019-08-19 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_dicom', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
