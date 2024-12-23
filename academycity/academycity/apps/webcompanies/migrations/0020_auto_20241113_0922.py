# Generated by Django 3.1.13 on 2024-11-13 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('webcompanies', '0019_auto_20221204_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webcompanies',
            name='target_ct',
            field=models.ForeignKey(blank=True, limit_choices_to={'model__in': ('accountingweb', 'businesssimweb', 'trainingweb', 'potentialweb', 'acmathweb', 'dlweb', 'mlweb', 'corporatevaluationweb', 'macroeconomicweb', 'fabhoseafricaweb', 'apewivesweb', 'radiusfoodweb', 'countries', 'institutionweb', 'checkcashingweb', 'tradesweb', 'portfolioweb', 'chweb')}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='webcompanies', to='contenttypes.contenttype'),
        ),
    ]
