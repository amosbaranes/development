# Generated by Django 3.1.13 on 2021-11-2  14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0049_new_is_links'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='subject_name',
            new_name='name',
        ),
    ]