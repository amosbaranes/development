# Generated by Django 3.0.10 on 2021-04-25 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fabhouseafrica', '0008_auto_20210425_0805'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalogsectioncategory',
            name='category_id',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='catalogsectioncategory',
            name='category_link',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='catalogsectioncategory',
            name='data_date',
            field=models.CharField(default='', max_length=20),
        ),
    ]
