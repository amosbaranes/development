# Generated by Django 3.1.13 on 2024-05-19 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('op', '0003_auto_20240510_1032'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stockreturnstd',
            options={'ordering': ['company__id', 'idx'], 'verbose_name': 'StockReturnStd', 'verbose_name_plural': 'StockReturnStds'},
        ),
    ]
