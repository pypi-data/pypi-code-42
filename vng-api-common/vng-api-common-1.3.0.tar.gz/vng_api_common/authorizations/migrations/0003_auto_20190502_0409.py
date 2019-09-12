# Generated by Django 2.1.8 on 2019-05-02 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("authorizations", "0002_authorizationsconfig")]

    operations = [
        migrations.AlterField(
            model_name="authorizationsconfig",
            name="api_root",
            field=models.URLField(
                default="https://ref.tst.vng.cloud/ac/api/v1",
                unique=True,
                verbose_name="api root",
            ),
        )
    ]
