# Generated by Django 3.0.10 on 2021-07-18 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0028_auto_20210718_1300'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='course_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='course_gradient_color_1',
            new_name='gradient_color_1',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='course_gradient_color_2',
            new_name='gradient_color_2',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='course_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='course_name_gradient_deg',
            new_name='name_gradient_deg',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='course_name_text_color',
            new_name='name_text_color',
        ),
        migrations.RenameField(
            model_name='program',
            old_name='program_title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='program',
            old_name='program_description',
            new_name='short_description',
        ),
        migrations.AddField(
            model_name='program',
            name='gradient_color_1',
            field=models.CharField(default='#969696', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='program',
            name='gradient_color_2',
            field=models.CharField(default='#dfdfdf', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='program',
            name='name_gradient_deg',
            field=models.IntegerField(blank=True, default=285),
        ),
        migrations.AddField(
            model_name='program',
            name='name_text_color',
            field=models.CharField(default='#090909', max_length=10, null=True),
        ),
    ]