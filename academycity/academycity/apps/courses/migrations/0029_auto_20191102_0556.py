# Generated by Django 2.1.10 on 2019-11-02 03:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0028_coursescheduleuser_team'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursescheduleteam',
            name='course_schedule',
        ),
        migrations.RemoveField(
            model_name='coursescheduleteam',
            name='description',
        ),
        migrations.RemoveField(
            model_name='coursescheduleteam',
            name='image',
        ),
        migrations.RemoveField(
            model_name='coursescheduleuser',
            name='name',
        ),
        migrations.RemoveField(
            model_name='coursescheduleuser',
            name='team',
        ),
        migrations.DeleteModel(
            name='CourseScheduleTeam',
        ),
    ]
