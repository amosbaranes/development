# Generated by Django 3.1.13 on 2023-03-29 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0043_auto_20230329_1539'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventorycategorys',
            old_name='Item_number',
            new_name='item_number',
        ),
    ]