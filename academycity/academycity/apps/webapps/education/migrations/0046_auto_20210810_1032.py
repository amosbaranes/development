# Generated by Django 3.0.10 on 2021-08-10 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0045_auto_20210807_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='gradient_color_1',
            field=models.CharField(default='#969696', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='gradient_color_2',
            field=models.CharField(default='#dfdfdf', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='name_text_color',
            field=models.CharField(default='#090909', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='new',
            name='gradient_color_1',
            field=models.CharField(default='#969696', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='new',
            name='gradient_color_2',
            field=models.CharField(default='#dfdfdf', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='new',
            name='name_text_color',
            field=models.CharField(default='#090909', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='gradient_color_1',
            field=models.CharField(default='#969696', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='gradient_color_2',
            field=models.CharField(default='#dfdfdf', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='name_text_color',
            field=models.CharField(default='#090909', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='gradient_color_1',
            field=models.CharField(default='#969696', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='gradient_color_2',
            field=models.CharField(default='#dfdfdf', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='name_text_color',
            field=models.CharField(default='#090909', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='gradient_color_1',
            field=models.CharField(default='#969696', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='gradient_color_2',
            field=models.CharField(default='#dfdfdf', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name_text_color',
            field=models.CharField(default='#090909', max_length=30, null=True),
        ),
    ]
