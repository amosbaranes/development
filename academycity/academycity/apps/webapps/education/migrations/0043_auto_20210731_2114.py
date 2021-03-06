# Generated by Django 3.0.10 on 2021-07-31 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0042_auto_20210730_0007'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutionweb',
            name='institute_name_color',
            field=models.CharField(blank=True, default='black', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='institutionweb',
            name='introduction_phrase_color',
            field=models.CharField(blank=True, default='black', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='institutionweb',
            name='search_explore_catalog_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='institutionweb',
            name='searching_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
