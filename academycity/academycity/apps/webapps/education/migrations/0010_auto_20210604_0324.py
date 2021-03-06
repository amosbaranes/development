# Generated by Django 3.1.11 on 2021-06-04 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0009_auto_20210603_0617'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutionweb',
            name='domain_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='institutionweb',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='institution/'),
        ),
        migrations.AddField(
            model_name='institutionweb',
            name='welcome_phrase',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
