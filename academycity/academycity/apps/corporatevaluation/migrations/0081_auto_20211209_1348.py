# Generated by Django 3.1.13 on 2021-12-09 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corporatevaluation', '0080_auto_20211209_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='xbrldimcompany',
            name='city',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='xbrldimcompany',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='xbrldimcompany',
            name='state',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='xbrldimcompany',
            name='zip',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='xbrldimcompany',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]