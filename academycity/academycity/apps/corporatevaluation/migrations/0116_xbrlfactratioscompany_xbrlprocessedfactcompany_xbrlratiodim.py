# Generated by Django 3.1.13 on 2023-06-28 08:48

import academycity.apps.core.sql
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corporatevaluation', '0115_auto_20230620_1742'),
    ]

    operations = [
        migrations.CreateModel(
            name='XBRLRatioDim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('industry', models.PositiveSmallIntegerField(default=0)),
                ('ratio_group', models.PositiveSmallIntegerField(default=0)),
                ('ratio_name', models.CharField(max_length=250, null=True)),
                ('numerator', models.IntegerField(default=0)),
                ('denominator', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'XBRL Dim Account',
                'verbose_name_plural': 'XBRL Dim Account',
                'ordering': ['industry', 'ratio_group'],
            },
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
        migrations.CreateModel(
            name='XBRLProcessedFactCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.IntegerField(default=0)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=18)),
                ('company', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='dim_processed_companies', to='corporatevaluation.xbrldimcompany')),
                ('time', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='dim_processed_times', to='corporatevaluation.xbrldimtime')),
            ],
            options={
                'verbose_name': 'XBRL Fact Company',
                'verbose_name_plural': 'XBRL Fact Companies',
            },
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
        migrations.CreateModel(
            name='XBRLFactRatiosCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=18)),
                ('company', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='dim_ratio_companies', to='corporatevaluation.xbrldimcompany')),
                ('ratio', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='dim_ratio_ratio', to='corporatevaluation.xbrlratiodim')),
                ('time', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='dim_ratio_times', to='corporatevaluation.xbrldimtime')),
            ],
            options={
                'verbose_name': 'XBRL Fact Ratios Company',
                'verbose_name_plural': 'XBRL Fact Ratios Companies',
            },
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
    ]
