# Generated by Django 3.1.11 on 2021-06-21 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkcashingchicago', '0016_auto_20210621_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='address1',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='address2',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='address3',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='address4',
            field=models.CharField(max_length=20, null=True),
        ),
    ]