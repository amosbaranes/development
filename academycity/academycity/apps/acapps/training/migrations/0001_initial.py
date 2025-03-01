# Generated by Django 3.1.13 on 2022-11-10 11:49

import academycity.apps.core.sql
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingWeb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('number_of_periods', models.SmallIntegerField(default=9)),
                ('number_of_participants', models.SmallIntegerField(default=9)),
                ('number_of_teams', models.SmallIntegerField(default=7)),
                ('max_participants_in_team', models.SmallIntegerField(default=6)),
            ],
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
    ]
