# Generated by Django 2.2 on 2019-04-30 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xform', '0002_attachment'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataDictionary',
            fields=[
                ('xform_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='xform.XForm')),
            ],
            bases=('xform.xform',),
        ),
    ]
