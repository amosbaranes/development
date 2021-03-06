# Generated by Django 2.1.10 on 2020-01-01 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corporatevaluation', '0007_auto_20191231_0056'),
    ]

    operations = [
        migrations.AddField(
            model_name='companydata',
            name='ebitda',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=18),
        ),
        migrations.AddField(
            model_name='companydata',
            name='effective_tax_rate',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=18),
        ),
        migrations.AddField(
            model_name='companydata',
            name='enterprise_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=18),
        ),
        migrations.AddField(
            model_name='companydata',
            name='ev_over_revenue',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=18),
        ),
        migrations.AddField(
            model_name='companydata',
            name='goodwill',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=18),
        ),
        migrations.AddField(
            model_name='companydata',
            name='income_taxes',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=18),
        ),
        migrations.AddField(
            model_name='companydata',
            name='intangible_assets_net_iad',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=18),
        ),
        migrations.AddField(
            model_name='companydata',
            name='interest_coverage_ratio',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=18),
        ),
        migrations.AddField(
            model_name='companydata',
            name='p_over_b_ratio',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=18),
        ),
        migrations.AddField(
            model_name='companydata',
            name='p_over_cash_flow_ratio',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=18),
        ),
        migrations.AddField(
            model_name='companydata',
            name='p_over_e_ratio',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=18),
        ),
        migrations.AddField(
            model_name='companydata',
            name='p_over_ebitda_ratio',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=18),
        ),
        migrations.AddField(
            model_name='companydata',
            name='p_over_s_ratio',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=18),
        ),
        migrations.AddField(
            model_name='companydata',
            name='total_long_term_debt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=18),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='city',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='state',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='zip',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
