# Generated by Django 3.1.13 on 2023-01-26 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0017_battalions_battalion_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='compliances',
            name='file_name',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
