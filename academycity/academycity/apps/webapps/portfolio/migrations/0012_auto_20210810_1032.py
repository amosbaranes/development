# Generated by Django 3.0.10 on 2021-08-10 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0011_auto_20210810_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='gradient_color_1',
            field=models.CharField(default='#969696', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='gradient_color_2',
            field=models.CharField(default='#dfdfdf', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='name_text_color',
            field=models.CharField(default='#090909', max_length=30, null=True),
        ),
    ]