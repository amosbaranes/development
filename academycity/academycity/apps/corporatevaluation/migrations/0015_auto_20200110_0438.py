# Generated by Django 2.1.10 on 2020-01-10 02:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporatevaluation', '0014_auto_20200109_1031'),
    ]

    operations = [
        migrations.RenameField(
            model_name='companydata',
            old_name='long_term_debt_current',
            new_name='long_term_debt_noncurrent',
        ),
    ]
