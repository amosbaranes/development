# Generated by Django 3.0.10 on 2021-04-24 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ugandatowns', '0021_conferencing'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conferencing',
            options={'ordering': ['active', '-created_date'], 'verbose_name': 'Conference', 'verbose_name_plural': 'Conferences'},
        ),
    ]
