# Generated by Django 3.1.13 on 2022-02-21 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20220213_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataadvancedtabs',
            name='tab_title',
            field=models.CharField(max_length=50, null=True),
        ),
    ]