# Generated by Django 3.1.13 on 2024-07-30 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ms', '0028_debug'),
    ]

    operations = [
        migrations.AddField(
            model_name='temp',
            name='dep_var_dim',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='dep_var_dim_temp_var', to='ms.genedim'),
        ),
    ]