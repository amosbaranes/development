# Generated by Django 2.1.10 on 2020-04-19 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corporatevaluation', '0021_auto_20200419_0320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydata',
            name='ebit',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=18),
        ),
    ]
