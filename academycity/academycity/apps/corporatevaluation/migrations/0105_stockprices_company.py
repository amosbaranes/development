# Generated by Django 3.1.13 on 2022-10-17 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corporatevaluation', '0104_stockprices'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockprices',
            name='company',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_info_stock_prices', to='corporatevaluation.xbrlcompanyinfo'),
        ),
    ]