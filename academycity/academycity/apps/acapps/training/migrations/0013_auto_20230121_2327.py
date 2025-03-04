# Generated by Django 3.1.13 on 2023-01-21 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0012_auto_20230120_0939'),
    ]

    operations = [
        migrations.RenameField(
            model_name='platoons',
            old_name='platon_name',
            new_name='platoon_name',
        ),
        migrations.AlterField(
            model_name='battalions',
            name='instructor',
            field=models.ManyToManyField(default=[1], related_name='instructor_battalions', to='training.Instructors'),
        ),
        migrations.AlterField(
            model_name='companys',
            name='instructor',
            field=models.ManyToManyField(default=[1], related_name='instructor_companys', to='training.Instructors'),
        ),
        migrations.AlterField(
            model_name='courses',
            name='instructor',
            field=models.ManyToManyField(default=[1], related_name='instructor_courses', to='training.Instructors'),
        ),
        migrations.AlterField(
            model_name='platoons',
            name='instructor',
            field=models.ManyToManyField(default=[1], related_name='instructor_platoons', to='training.Instructors'),
        ),
        migrations.AlterField(
            model_name='soldiers',
            name='course',
            field=models.ManyToManyField(default=[1], related_name='course_soldiers', to='training.Courses'),
        ),
    ]
