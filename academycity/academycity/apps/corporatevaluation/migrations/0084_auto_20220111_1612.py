# Generated by Django 3.1.13 on 2022-01-11 14:12

import academycity.apps.core.sql
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corporatevaluation', '0083_auto_20211209_1538'),
    ]

    operations = [
        migrations.CreateModel(
            name='XBRLRealEquityPrices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10)),
                ('t', models.PositiveBigIntegerField(default=0)),
                ('o', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('h', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('l', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('c', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('v', models.PositiveBigIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'XBRLRealEquityPrices',
                'verbose_name_plural': 'XBRLRealEquityPrices',
                'ordering': ['ticker'],
            },
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
        migrations.AlterModelOptions(
            name='xbrldimcompany',
            options={'ordering': ['main_sic_code', 'sic_code', 'company_name'], 'verbose_name': 'XBRL Dim Company', 'verbose_name_plural': 'XBRL Dim Companies'},
        ),
        migrations.AlterField(
            model_name='xbrlspearningforecast',
            name='quarter',
            field=models.PositiveSmallIntegerField(blank=True, default=1),
        ),
        migrations.AlterField(
            model_name='xbrlspearningforecast',
            name='year',
            field=models.PositiveSmallIntegerField(blank=True, default=2022),
        ),
        migrations.CreateModel(
            name='XBRLSPStrategies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('previous_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('current_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('condor_price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('call_delta_low', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('call_strike_low', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('call_price_low', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('call_delta_high', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('call_strike_high', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('call_price_high', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('put_delta_low', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('put_strike_low', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('put_price_low', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('put_delta_high', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('put_strike_high', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('put_price_high', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('company', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='company_strategies', to='corporatevaluation.xbrlcompanyinfo')),
            ],
            options={
                'verbose_name': 'XBRLSPStrategy',
                'verbose_name_plural': 'XBRLSPStrategies',
                'ordering': ['company'],
            },
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
    ]
