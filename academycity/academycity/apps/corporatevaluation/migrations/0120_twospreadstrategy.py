# Generated by Django 3.1.13 on 2023-12-17 17:27

import academycity.apps.core.sql
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corporatevaluation', '0119_auto_20231004_1149'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwoSpreadStrategy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strategy_idx', models.PositiveBigIntegerField(default=0)),
                ('strike', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('company', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='two_spread_strategys', to='corporatevaluation.xbrlcompanyinfo')),
            ],
            options={
                'verbose_name': 'TwoSpreadStrategy',
                'verbose_name_plural': 'TwoSpreadStrategys',
                'ordering': ['strategy_idx'],
            },
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
    ]