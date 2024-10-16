# Generated by Django 3.1.13 on 2023-06-01 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0061_auto_20230530_1507'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventorycategorys',
            options={'ordering': ['category_name'], 'verbose_name': 'inventorycategory', 'verbose_name_plural': 'inventorycategorys'},
        ),
        migrations.AlterModelOptions(
            name='inventorys',
            options={'ordering': ['item_number'], 'verbose_name': 'inventory', 'verbose_name_plural': 'inventorys'},
        ),
        migrations.RenameField(
            model_name='inventorys',
            old_name='inventory_number',
            new_name='item_name',
        ),
        migrations.RenameField(
            model_name='soldiers',
            old_name='sport_size',
            new_name='clothes_size',
        ),
        migrations.RemoveField(
            model_name='inventorycategorys',
            name='category_name_1',
        ),
        migrations.RemoveField(
            model_name='inventorycategorys',
            name='category_name_2',
        ),
        migrations.RemoveField(
            model_name='inventorycategorys',
            name='item_number',
        ),
        migrations.RemoveField(
            model_name='inventorycategorys',
            name='pn',
        ),
        migrations.RemoveField(
            model_name='soldiers',
            name='gun_mz4psn',
        ),
        migrations.RemoveField(
            model_name='soldiers',
            name='gun_ramonsn',
        ),
        migrations.RemoveField(
            model_name='soldiers',
            name='uniform_size',
        ),
        migrations.AddField(
            model_name='inventorys',
            name='description',
            field=models.CharField(blank=True, default='', max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='inventorys',
            name='qty_per_soldier',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='inventorys',
            name='item_number',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
    ]
