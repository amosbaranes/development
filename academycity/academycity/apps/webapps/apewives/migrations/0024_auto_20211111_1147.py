# Generated by Django 3.1.13 on 2021-11-11 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apewives', '0023_auto_20211111_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apewivesweb',
            name='about_text_1',
            field=models.TextField(blank=True, default=''),
        ),
    ]
