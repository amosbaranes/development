# Generated by Django 3.1.13 on 2023-01-12 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corporatevaluation', '0110_auto_20221020_0753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xbrlspearningforecast',
            name='quarter',
            field=models.PositiveSmallIntegerField(blank=True, default=1),
        ),
        migrations.AlterField(
            model_name='xbrlspearningforecast',
            name='year',
            field=models.PositiveSmallIntegerField(blank=True, default=2023),
        ),
    ]
