# Generated by Django 3.1.13 on 2023-10-04 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0073_inventoryunitfact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorys',
            name='item_name',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
