# Generated by Django 3.1.11 on 2021-06-21 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkcashingchicago', '0017_auto_20210621_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='address1',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='address2',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='address3',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='address4',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
