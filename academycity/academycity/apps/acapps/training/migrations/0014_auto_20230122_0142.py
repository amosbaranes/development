# Generated by Django 3.1.13 on 2023-01-21 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0013_auto_20230121_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='soldiers',
            name='mz4psn',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='soldiers',
            name='ramonsn',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]