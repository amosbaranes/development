# Generated by Django 3.0.10 on 2021-09-09 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corporatevaluation', '0046_xbrlvaluationaccounts_scale'),
    ]

    operations = [
        migrations.AddField(
            model_name='xbrlregion',
            name='full_name',
            field=models.CharField(blank=True, default='', max_length=128, null=True),
        ),
    ]