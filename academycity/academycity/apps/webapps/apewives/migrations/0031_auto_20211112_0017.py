# Generated by Django 3.1.13 on 2021-11-11 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apewives', '0030_auto_20211112_0008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apewivesweb',
            name='verification_text_1',
        ),
        migrations.RemoveField(
            model_name='apewivesweb',
            name='verification_text_2',
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='contract_address_text_paragraph',
            field=models.TextField(blank=True, null=True),
        ),
    ]