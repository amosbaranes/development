# Generated by Django 3.1.13 on 2024-06-16 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0003_temp_dep_var_dim'),
    ]

    operations = [
        migrations.AddField(
            model_name='factnormalizedminmax',
            name='dip_var_dim',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='dep_var_dim_fact_normalized_minmax', to='covid.vardim'),
        ),
    ]