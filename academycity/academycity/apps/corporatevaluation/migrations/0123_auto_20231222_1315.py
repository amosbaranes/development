# Generated by Django 3.1.13 on 2023-12-22 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporatevaluation', '0122_twospreadstrategydetails_seconds'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='twospreadstrategydetails',
            options={'ordering': ['stock_price'], 'verbose_name': 'TwoSpreadStrategyDetail', 'verbose_name_plural': 'TwoSpreadStrategyDetails'},
        ),
    ]