# Generated by Django 3.0.10 on 2021-08-11 23:17

import academycity.apps.core.sql
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corporatevaluation', '0029_xbrlindustryinfo_xbrlmainindustryinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='XBRLCompanyInfoInProcess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exchange', models.CharField(default='nyse', max_length=10)),
                ('company_name', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('ticker', models.CharField(max_length=10)),
                ('company_letter', models.CharField(default='', max_length=1)),
                ('is_error', models.BooleanField(default=False)),
                ('message', models.CharField(max_length=500, null=True)),
            ],
            options={
                'verbose_name': 'Company Info',
                'verbose_name_plural': 'Company Info',
                'ordering': ['company_name'],
            },
            bases=(academycity.apps.core.sql.TruncateTableMixin, models.Model),
        ),
    ]
