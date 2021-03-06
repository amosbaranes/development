# Generated by Django 2.1.10 on 2020-01-09 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corporatevaluation', '0012_auto_20200105_0142'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companydata',
            options={'ordering': ['company', 'year'], 'verbose_name': 'Company Data', 'verbose_name_plural': 'Company Data'},
        ),
        migrations.AlterModelOptions(
            name='companyinfo',
            options={'ordering': ['company_name'], 'verbose_name': 'Company Info', 'verbose_name_plural': 'Company Info'},
        ),
        migrations.AlterModelOptions(
            name='industry',
            options={'ordering': ['sic_description'], 'verbose_name': 'Industry', 'verbose_name_plural': 'Industry'},
        ),
        migrations.AddField(
            model_name='companydata',
            name='stockholders_quity',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=18),
        ),
        migrations.AlterField(
            model_name='companydata',
            name='company',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='company_data', to='corporatevaluation.CompanyInfo'),
        ),
    ]
