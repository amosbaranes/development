# Generated by Django 3.0.10 on 2021-05-10 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RadiusFoodWeb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, default='', max_length=200)),
                ('image_logo', models.ImageField(default='radius_food_web/no_image.png', upload_to='radius_food_web')),
                ('office_address_1', models.CharField(blank=True, default='', max_length=100)),
                ('office_address_2', models.CharField(blank=True, default='', max_length=100)),
            ],
            options={
                'verbose_name': 'radius_food_web',
                'verbose_name_plural': 'radius_food_webs',
            },
        ),
    ]