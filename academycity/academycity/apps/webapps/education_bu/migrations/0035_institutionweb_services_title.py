# Generated by Django 3.0.10 on 2021-07-2  16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0034_institutionweb_courses_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutionweb',
            name='services_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
