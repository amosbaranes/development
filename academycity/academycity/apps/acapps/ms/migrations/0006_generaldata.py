# Generated by Django 3.1.13 on 2023-03-25 01:18

import academycity.apps.core.sql
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ms', '0005_auto_20230321_1653'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_name', models.CharField(blank=True, default='', max_length=40, null=True)),
                ('data_json', models.JSONField(null=True)),
            ],
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
    ]