# Generated by Django 3.1.13 on 2023-07-04 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0069_adjectives_adjectivesvalues'),
    ]

    operations = [
        migrations.AddField(
            model_name='soldiers',
            name='mz10',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]