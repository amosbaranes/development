# Generated by Django 2.1.10 on 2019-09-15 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_courseschedule_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sectiontranslation',
            name='slug',
            field=models.SlugField(blank=True, default='', help_text='Please supply the section slug.', max_length=128, verbose_name='slug'),
        ),
    ]
