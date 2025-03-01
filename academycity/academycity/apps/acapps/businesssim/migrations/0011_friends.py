# Generated by Django 3.1.13 on 2022-10-23 12:00

import academycity.apps.core.sql
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businesssim', '0010_auto_20220924_2215'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('friends', models.JSONField(null=True)),
            ],
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
    ]
