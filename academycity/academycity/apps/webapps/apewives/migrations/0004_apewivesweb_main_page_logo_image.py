# Generated by Django 3.1.13 on 2021-11-10 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apewives', '0003_auto_20211110_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='apewivesweb',
            name='main_page_logo_image',
            field=models.ImageField(default='apewives_web/home/no_image.png', upload_to='apewives_web/home'),
        ),
    ]