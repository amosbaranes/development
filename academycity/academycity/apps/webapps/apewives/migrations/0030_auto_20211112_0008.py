# Generated by Django 3.1.13 on 2021-11-11 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apewives', '0029_auto_20211112_0002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apewivesweb',
            name='ownership_text',
        ),
        migrations.RemoveField(
            model_name='apewivesweb',
            name='ownership_text_2',
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='ownership_text_paragraph',
            field=models.TextField(blank=True, null=True),
        ),
    ]