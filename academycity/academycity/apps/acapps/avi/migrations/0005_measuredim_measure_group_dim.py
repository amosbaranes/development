# Generated by Django 3.1.13 on 2022-11-26 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('avi', '0004_measuregroupdim'),
    ]

    operations = [
        migrations.AddField(
            model_name='measuredim',
            name='measure_group_dim',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='country_dim_world_Bank_fact', to='avi.measuregroupdim'),
        ),
    ]
