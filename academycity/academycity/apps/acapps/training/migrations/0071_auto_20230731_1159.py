# Generated by Django 3.1.13 on 2023-07-31 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0070_soldiers_mz10'),
    ]

    operations = [
        migrations.RenameField(
            model_name='soldiers',
            old_name='sub_profession',
            new_name='professional_qualified',
        ),
        migrations.AddField(
            model_name='inventorys',
            name='critical',
            field=models.CharField(blank=True, default='1', max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='soldiers',
            name='function',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
    ]