# Generated by Django 3.1.13 on 2023-06-17 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0066_auto_20230617_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='complianceweeks',
            name='week_start_day',
            field=models.PositiveIntegerField(default=20230101),
        ),
        migrations.AlterField(
            model_name='complianceweeks',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]