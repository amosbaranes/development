# Generated by Django 3.1.13 on 2023-03-27 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0040_delete_generaldata'),
    ]

    operations = [
        migrations.AddField(
            model_name='testsvariables',
            name='down_color',
            field=models.CharField(blank=True, default='red', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='testsvariables',
            name='down_value',
            field=models.SmallIntegerField(default=70),
        ),
        migrations.AddField(
            model_name='testsvariables',
            name='other_color',
            field=models.CharField(blank=True, default='yellow', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='testsvariables',
            name='up_color',
            field=models.CharField(blank=True, default='green', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='testsvariables',
            name='up_value',
            field=models.SmallIntegerField(default=70),
        ),
    ]