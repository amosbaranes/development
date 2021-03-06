# Generated by Django 2.1.10 on 2019-11-03 10:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0032_auto_20191103_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='instructors',
            field=models.ManyToManyField(default=1, limit_choices_to={'groups__name__in': 'instructors'}, related_name='user_instructors', to=settings.AUTH_USER_MODEL),
        ),
    ]
