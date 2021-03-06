# Generated by Django 2.1.10 on 2020-06-08 02:40

import academycity.apps.core.fields
import cms.models.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0053_auto_20200510_0420'),
        ('cms', '0022_auto_20180620_1551'),
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('globsim', '0023_auto_20200607_1838'),
    ]

    operations = [
        migrations.CreateModel(
            name='DistributorAttribute',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('order', academycity.apps.core.fields.OrderField(blank=True, default=1)),
                ('description', cms.models.fields.PlaceholderField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, slotname='attribute_description', to='cms.Placeholder')),
                ('distributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='distributor_attributes', to='globsim.Distributor')),
                ('image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.FILER_IMAGE_MODEL)),
            ],
            options={
                'verbose_name': 'distributor_attribute',
                'verbose_name_plural': 'distributor_attributes',
                'ordering': ['order'],
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='DistributorAttributeTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(default='', help_text='Please supply the section name.', max_length=128, verbose_name='name')),
                ('slug', models.SlugField(blank=True, default='', help_text='Please supply the section slug.', max_length=128, verbose_name='slug')),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='globsim.DistributorAttribute')),
            ],
            options={
                'verbose_name': 'distributor_attribute Translation',
                'db_table': 'globsim_distributorattribute_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='DistributorSegment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('percentage', models.IntegerField(default=50)),
                ('distributor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='distributor_segments', to='globsim.Distributor')),
                ('segment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='segment_distributors', to='globsim.Segment')),
            ],
            options={
                'verbose_name': 'distributor',
                'verbose_name_plural': 'distributors',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='GDistributor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_period', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_period_g_distributors', to='globsim.Period')),
                ('distributor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='g_distributor', to='globsim.Distributor')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_g_distributors', to='courses.Team')),
            ],
            options={
                'verbose_name': 'g_distributor',
                'verbose_name_plural': 'g_distributors',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='GDistributorPeriodData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('g_distributor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='g_distributor_periods_data', to='globsim.GDistributor')),
                ('period', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='period_g_distributors_data', to='globsim.Period')),
            ],
            options={
                'verbose_name': 'product data',
                'verbose_name_plural': 'products data',
            },
        ),
        migrations.CreateModel(
            name='GDistributorPeriodDataDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField(default=1)),
                ('type', models.IntegerField(choices=[(10, 'Distributor_Retail_margin'), (110, 'Distributor_Extra_support')], default=0)),
                ('g_distributor_data', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='g_distributor_period_data_details', to='globsim.GDistributorPeriodData')),
            ],
            options={
                'verbose_name': 'g_distributor_data_detail',
                'verbose_name_plural': 'g_distributor_data_details',
                'ordering': ['type'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='distributorattributetranslation',
            unique_together={('language_code', 'master')},
        ),
    ]
