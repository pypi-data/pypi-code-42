# Generated by Django 2.2.3 on 2019-08-23 20:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('multifactor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userkey',
            name='key_type',
            field=models.CharField(choices=[('FIDO2', 'FIDO2 Security Device'), ('U2F', 'U2F Security Key'), ('TOTP', 'TOTP Authenticator')], max_length=25),
        ),
        migrations.CreateModel(
            name='DisabledFallback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fallback', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
