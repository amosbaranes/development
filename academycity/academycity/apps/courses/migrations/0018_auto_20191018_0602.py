# Generated by Django 2.1.10 on 2019-10-18 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0017_auto_20191018_0544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chartofaccounts',
            name='parent',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
