# Generated by Django 3.0.10 on 2021-08-08 08:19

import cms.models.fields
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('portfolio', '0009_auto_20210716_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='full_description',
            field=cms.models.fields.PlaceholderField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, slotname='full_description', to='cms.Placeholder'),
        ),
    ]