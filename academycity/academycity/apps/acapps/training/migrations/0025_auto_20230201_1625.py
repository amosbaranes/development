# Generated by Django 3.1.13 on 2023-02-01 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0024_testsforevents'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='soldiers',
            name='pant_size',
        ),
        migrations.RemoveField(
            model_name='soldiers',
            name='shirt_size',
        ),
        migrations.AddField(
            model_name='soldiers',
            name='sport_size',
            field=models.CharField(blank=True, default='', max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='soldiers',
            name='uniform_size',
            field=models.CharField(blank=True, default='', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='soldiers',
            name='shoes_size',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
    ]
