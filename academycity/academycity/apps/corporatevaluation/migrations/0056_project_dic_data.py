# Generated by Django 3.1.13 on 2021-09-27 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corporatevaluation', '0055_xbrlcompanyinfo_financial_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='dic_data',
            field=models.JSONField(null=True),
        ),
    ]
