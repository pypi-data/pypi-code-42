# Generated by Django 2.2.5 on 2019-09-12 10:02

from django.db import migrations, models


def fill_default_aggregator_for(apps, schema_editor):
    Application = apps.get_model("authent", "Application")
    Provider = apps.get_model("mds", "Provider")

    for application in Application.objects.all():
        if application.owner:
            try:
                provider = Provider.objects.get(pk=application.owner)
                application.aggregator_for.add(provider)
            except Provider.DoesNotExist:
                pass


class Migration(migrations.Migration):
    atomic = False

    dependencies = [("authent", "0003_pre_add_aggregator_for_application")]

    operations = [
        migrations.RunPython(fill_default_aggregator_for, migrations.RunPython.noop)
    ]
