# Generated by Django 3.1.13 on 2022-01-11 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataTabs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tab_name', models.CharField(max_length=100, null=True)),
                ('tab_text', models.TextField(null=True)),
            ],
        ),
    ]