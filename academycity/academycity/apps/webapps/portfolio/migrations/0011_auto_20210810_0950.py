# Generated by Django 3.0.10 on 2021-08-10 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0010_service_full_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='gradient_color_1',
            field=models.CharField(default='#969696', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='gradient_color_2',
            field=models.CharField(default='#dfdfdf', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='name_gradient_deg',
            field=models.IntegerField(blank=True, default=285),
        ),
        migrations.AddField(
            model_name='service',
            name='name_text_color',
            field=models.CharField(default='#090909', max_length=10, null=True),
        ),
    ]