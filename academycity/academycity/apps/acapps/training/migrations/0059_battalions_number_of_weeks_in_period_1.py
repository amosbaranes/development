# Generated by Django 3.1.13 on 2023-05-26 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0058_auto_20230525_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='battalions',
            name='number_of_weeks_in_period_1',
            field=models.SmallIntegerField(default=9),
        ),
    ]