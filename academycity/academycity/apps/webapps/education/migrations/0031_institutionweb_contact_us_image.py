# Generated by Django 3.0.10 on 2021-07-18 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0030_course_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutionweb',
            name='contact_us_image',
            field=models.ImageField(blank=True, null=True, upload_to='institution/'),
        ),
    ]
