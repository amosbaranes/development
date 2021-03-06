# Generated by Django 2.1.10 on 2020-04-09 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporatevaluation', '0015_auto_20200110_0438'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companydatatimeseries',
            name='team',
        ),
        migrations.RemoveField(
            model_name='companydatatimeseries',
            name='type',
        ),
        migrations.RemoveField(
            model_name='teamcompany',
            name='company_info',
        ),
        migrations.RemoveField(
            model_name='teamcompany',
            name='industry',
        ),
        migrations.RemoveField(
            model_name='teamcompany',
            name='team',
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['id'], 'verbose_name': 'project', 'verbose_name_plural': 'projects'},
        ),
        migrations.DeleteModel(
            name='CompanyDataTimeSeries',
        ),
        migrations.DeleteModel(
            name='CompanyDataType',
        ),
        migrations.DeleteModel(
            name='TeamCompany',
        ),
    ]
