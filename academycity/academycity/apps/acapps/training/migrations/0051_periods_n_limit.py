# Generated by Django 3.1.13 on 2023-04-09 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0050_testevents_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='periods',
            name='n_limit',
            field=models.SmallIntegerField(default=2),
        ),
    ]