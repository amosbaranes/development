# Generated by Django 3.1.13 on 2021-11-10 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apewives', '0018_auto_20211111_0141'),
    ]

    operations = [
        migrations.AddField(
            model_name='apewivesweb',
            name='footer_desc',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='footer_title_1',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='footer_title_2',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='verification_text_1',
            field=models.CharField(blank=True, default='', max_length=512),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='verification_text_2',
            field=models.CharField(blank=True, default='', max_length=512),
        ),
    ]