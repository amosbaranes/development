# Generated by Django 3.1.13 on 2023-02-09 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20220925_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debug',
            name='value',
            field=models.CharField(max_length=1024),
        ),
    ]