# Generated by Django 3.0.10 on 2021-07-28 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporatevaluation', '0027_todolist'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todolist',
            options={'ordering': ['-is_active', '-priority'], 'verbose_name': 'todolist', 'verbose_name_plural': 'todolist'},
        ),
    ]