# Generated by Django 3.1.13 on 2022-11-14 12:13

import academycity.apps.core.sql
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('avi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeasureDim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measure_name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('measure_code', models.CharField(blank=True, default='', max_length=100, null=True)),
            ],
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
        migrations.AddField(
            model_name='worldbankfact',
            name='measure_dim',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='country_dim_world_Bank_fact', to='avi.measuredim'),
        ),
    ]
