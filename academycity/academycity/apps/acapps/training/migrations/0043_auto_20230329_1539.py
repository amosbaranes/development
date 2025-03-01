# Generated by Django 3.1.13 on 2023-03-29 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0042_periods'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventorycategorys',
            options={'ordering': ['category', 'category_name_1'], 'verbose_name': 'inventorycategory', 'verbose_name_plural': 'inventorycategorys'},
        ),
        migrations.AlterModelOptions(
            name='periods',
            options={'ordering': ['battalion', 'period_number'], 'verbose_name': 'period', 'verbose_name_plural': 'periods'},
        ),
        migrations.RemoveField(
            model_name='inventorycategorys',
            name='category_name',
        ),
        migrations.AddField(
            model_name='inventorycategorys',
            name='Item_number',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='inventorycategorys',
            name='category',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='inventorycategorys',
            name='category_name_1',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='inventorycategorys',
            name='category_name_2',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='inventorycategorys',
            name='pn',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='inventorys',
            name='item_number',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='inventorys',
            name='pn',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
