# Generated by Django 3.1.11 on 2021-07-05 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('webcompanies', '0007_auto_20210617_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webcompanies',
            name='target_ct',
            field=models.ForeignKey(blank=True, limit_choices_to={'model__in': ('fabhoseafricaweb', 'bizlandweb', 'radiusfoodweb', 'countries', 'institutionweb', 'checkcashingweb', 'portfolioweb')}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='webcompanies', to='contenttypes.contenttype'),
        ),
    ]