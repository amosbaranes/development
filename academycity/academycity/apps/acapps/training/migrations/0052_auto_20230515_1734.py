# Generated by Django 3.1.13 on 2023-05-15 14:34

import academycity.apps.core.sql
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0051_periods_n_limit'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComplianceDays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_unit', models.JSONField(null=True)),
            ],
            options={
                'verbose_name': 'compliance_day',
                'verbose_name_plural': 'compliance_days',
            },
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ComplianceWeeks',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('unit', models.IntegerField(blank=True, null=True)),
                ('conclusion', models.TextField(blank=True, null=True)),
                ('battalion', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='battalion_compliance_weeks', to='training.battalions')),
            ],
            options={
                'verbose_name': 'compliance_week',
                'verbose_name_plural': 'compliance_weeks',
            },
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
        migrations.CreateModel(
            name='DoubleShootMembers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ds_id', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('ds_name', models.CharField(blank=True, default='', max_length=128, null=True)),
            ],
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
        migrations.RemoveField(
            model_name='compliances',
            name='platoon',
        ),
        migrations.RemoveField(
            model_name='compliancewithplans',
            name='battalion',
        ),
        migrations.DeleteModel(
            name='ComplianceDay',
        ),
        migrations.DeleteModel(
            name='Compliances',
        ),
        migrations.DeleteModel(
            name='ComplianceWithPlans',
        ),
        migrations.AddField(
            model_name='compliancedays',
            name='compliance_week',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='compliance_week_compliance_days', to='training.complianceweeks'),
        ),
        migrations.AddField(
            model_name='compliancedays',
            name='time_dim',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='time_dim_compliance_days', to='training.timedim'),
        ),
    ]
