# Generated by Django 3.1.13 on 2021-12-09 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corporatevaluation', '0079_xbrlspstatistics_mean_abs_actual_forecast_change_money'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xbrldimtime',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]