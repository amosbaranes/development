# Generated by Django 3.1.13 on 2023-09-04 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ms', '0008_delete_generaldata'),
    ]

    operations = [
        migrations.AddField(
            model_name='genedim',
            name='reduced_clusters',
            field=models.JSONField(null=True),
        ),
    ]