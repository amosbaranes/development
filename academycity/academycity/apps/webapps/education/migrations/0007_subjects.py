# Generated by Django 3.1.11 on 2021-06-02 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0006_auto_20210602_1015'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, default=1000)),
                ('image', models.ImageField(blank=True, null=True, upload_to='subjects/')),
                ('subject_name', models.CharField(max_length=100, null=True)),
                ('is_popular', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'subject',
                'verbose_name_plural': 'subjects',
                'ordering': ['order'],
            },
        ),
    ]