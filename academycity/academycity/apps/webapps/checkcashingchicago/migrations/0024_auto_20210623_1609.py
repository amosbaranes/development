# Generated by Django 3.1.11 on 2021-06-23 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkcashingchicago', '0023_location_location_detail_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='south_suburbs_sort',
        ),
        migrations.AlterField(
            model_name='location',
            name='check_cashing_web',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='checkcashingchicago.checkcashingweb'),
        ),
        migrations.CreateModel(
            name='LocationRegion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, default=1000)),
                ('region_title', models.CharField(max_length=100, null=True)),
                ('slug', models.SlugField(max_length=250, null=True)),
                ('check_cashing_web', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location_regions', to='checkcashingchicago.checkcashingweb')),
            ],
            options={
                'verbose_name': 'location_region',
                'verbose_name_plural': 'location_regions',
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='location',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='region_locations', to='checkcashingchicago.locationregion'),
        ),
    ]