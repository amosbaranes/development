# Generated by Django 3.1.13 on 2024-09-05 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ms', '0031_factnormalizedminmax'),
    ]

    operations = [
        migrations.AddField(
            model_name='factnormalized',
            name='run_number',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='factnormalizedtemp',
            name='run_number',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
    ]