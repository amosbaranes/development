# Generated by Django 2.1.10 on 2020-04-18 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0051_auto_20200418_0804'),
        ('corporatevaluation', '0018_remove_project_course_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='course_schedule',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project', to='courses.CourseSchedule'),
        ),
    ]
