# Generated by Django 3.1.13 on 2023-08-29 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('avic', '0002_countrygroupdim'),
    ]

    operations = [
        migrations.AddField(
            model_name='countrydim',
            name='country_group_dim',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='country_dim_group_dim', to='avic.countrygroupdim'),
        ),
    ]