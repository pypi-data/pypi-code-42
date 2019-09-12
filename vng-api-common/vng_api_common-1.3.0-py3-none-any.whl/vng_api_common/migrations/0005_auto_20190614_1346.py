# Generated by Django 2.1.1 on 2019-06-14 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("vng_api_common", "0004_auto_20190517_0903")]

    operations = [
        migrations.AlterField(
            model_name="apicredential",
            name="api_root",
            field=models.URLField(
                help_text="URL of the external API, ending in a trailing slash. Example: https://example.com/api/v1/",
                unique=True,
                verbose_name="API-root",
            ),
        ),
        migrations.AlterField(
            model_name="apicredential",
            name="client_id",
            field=models.CharField(
                help_text="Client ID to identify this API at the external API.",
                max_length=255,
                verbose_name="client ID",
            ),
        ),
        migrations.AlterField(
            model_name="apicredential",
            name="label",
            field=models.CharField(
                default="",
                help_text="Human readable label of the external API.",
                max_length=100,
                verbose_name="label",
            ),
        ),
        migrations.AlterField(
            model_name="apicredential",
            name="secret",
            field=models.CharField(
                help_text="Secret belonging to the client ID.",
                max_length=255,
                verbose_name="secret",
            ),
        ),
        migrations.AlterField(
            model_name="apicredential",
            name="user_id",
            field=models.CharField(
                help_text="User ID to use for the audit trail. Although these external API credentials are typically used bythis API itself instead of a user, the user ID is required.",
                max_length=255,
                verbose_name="user ID",
            ),
        ),
        migrations.AlterField(
            model_name="apicredential",
            name="user_representation",
            field=models.CharField(
                default="",
                help_text="Human readable representation of the user.",
                max_length=255,
                verbose_name="user representation",
            ),
        ),
        migrations.AlterField(
            model_name="jwtsecret",
            name="identifier",
            field=models.CharField(
                help_text="Client ID to identify external API's and applications that access this API.",
                max_length=50,
                unique=True,
                verbose_name="client ID",
            ),
        ),
        migrations.AlterField(
            model_name="jwtsecret",
            name="secret",
            field=models.CharField(
                help_text="Secret belonging to the client ID.",
                max_length=255,
                verbose_name="secret",
            ),
        ),
    ]
