# Generated by Django 2.1.10 on 2020-05-02 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0051_auto_20200418_0804'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coursescheduleuser',
            options={'ordering': ['course_schedule', 'team', 'user'], 'verbose_name': 'course schedule user', 'verbose_name_plural': 'courses schedule user'},
        ),
    ]
