# Generated by Django 3.1.13 on 2021-11-15 19:29

import academycity.apps.core.sql
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corporatevaluation', '0073_auto_20211115_1628'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='xbrlcountryyeardata',
            options={'ordering': ['country', 'year'], 'verbose_name': 'XBRL Country Year Data', 'verbose_name_plural': 'XBRL Countries Year Data'},
        ),
        migrations.AddField(
            model_name='xbrlregionsofoperations',
            name='rating',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='xbrlregionsofoperations',
            name='risk_premium',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='xbrlregionsofoperations',
            name='spread',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='xbrlregionsofoperations',
            name='tax_rate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.CreateModel(
            name='XBRLRegionYearData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveSmallIntegerField(default=0)),
                ('tax_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('moodys_rate_completed_by_sp', models.CharField(default='', max_length=20)),
                ('rating_based_default_spread', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('country_risk_premium_rating', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('region', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='region_data', to='corporatevaluation.xbrlregion')),
            ],
            options={
                'verbose_name': 'XBRL Region Year Data',
                'verbose_name_plural': 'XBRL Regions Year Data',
                'ordering': ['region', 'year'],
            },
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
    ]
