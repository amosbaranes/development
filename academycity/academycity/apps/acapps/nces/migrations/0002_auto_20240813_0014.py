# Generated by Django 3.1.13 on 2024-08-12 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nces', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fact',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True),
        ),
    ]