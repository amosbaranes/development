# Generated by Django 3.1.13 on 2023-06-01 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0062_auto_20230601_2107'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventoryfact',
            options={'verbose_name': 'inventory_fact', 'verbose_name_plural': 'inventory_facts'},
        ),
        migrations.AlterField(
            model_name='inventoryfact',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
    ]