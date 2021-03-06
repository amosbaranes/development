# Generated by Django 3.0.10 on 2021-07-18 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0027_auto_20210715_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_gradient_color_1',
            field=models.CharField(default='#969696', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='course_gradient_color_2',
            field=models.CharField(default='#dfdfdf', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='course_name_gradient_deg',
            field=models.IntegerField(blank=True, default=285),
        ),
        migrations.AddField(
            model_name='course',
            name='course_name_text_color',
            field=models.CharField(default='#090909', max_length=10, null=True),
        ),
    ]
