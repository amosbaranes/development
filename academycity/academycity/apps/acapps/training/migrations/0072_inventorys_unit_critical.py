# Generated by Django 3.1.13 on 2023-09-03 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0071_auto_20230731_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorys',
            name='unit_critical',
            field=models.CharField(blank=True, default='1', max_length=32, null=True),
        ),
    ]
