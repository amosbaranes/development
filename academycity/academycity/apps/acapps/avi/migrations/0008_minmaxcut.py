# Generated by Django 3.1.13 on 2023-01-29 07:50

import academycity.apps.core.sql
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('avi', '0007_countrydim_country_cc'),
    ]

    operations = [
        migrations.CreateModel(
            name='MinMaxCut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min', models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=16, null=True)),
                ('max', models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=16, null=True)),
                ('measure_dim', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='country_dim_min_max_cut', to='avi.measuredim')),
                ('time_dim', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='time_dim_min_max_cut', to='avi.timedim')),
            ],
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
    ]
