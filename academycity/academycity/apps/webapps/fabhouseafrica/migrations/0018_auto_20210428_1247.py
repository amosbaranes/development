# Generated by Django 3.0.10 on 2021-04-28 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fabhouseafrica', '0017_auto_20210428_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='about',
            name='Fabulous_title',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='about',
            name='about_us_image',
            field=models.ImageField(default='fab_hose_africa_web/no_image.png', upload_to='fab_hose_africa_web/about'),
        ),
        migrations.AddField(
            model_name='about',
            name='about_us_title',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='about',
            name='background_image',
            field=models.ImageField(default='fab_hose_africa_web/no_image.png', upload_to='fab_hose_africa_web/about'),
        ),
        migrations.AddField(
            model_name='about',
            name='believe_image',
            field=models.ImageField(default='fab_hose_africa_web/no_image.png', upload_to='fab_hose_africa_web/about/believe'),
        ),
        migrations.AddField(
            model_name='about',
            name='believe_phrase',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='about',
            name='company_history',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='about',
            name='company_history_image_left',
            field=models.ImageField(default='fab_hose_africa_web/no_image.png', upload_to='fab_hose_africa_web/about/history'),
        ),
        migrations.AddField(
            model_name='about',
            name='company_history_image_right',
            field=models.ImageField(default='fab_hose_africa_web/no_image.png', upload_to='fab_hose_africa_web/about/history'),
        ),
        migrations.AddField(
            model_name='about',
            name='company_legacy',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='about',
            name='left_believe_phrase',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
        migrations.AddField(
            model_name='about',
            name='mission_image',
            field=models.ImageField(default='fab_hose_africa_web/no_image.png', upload_to='fab_hose_africa_web/about'),
        ),
        migrations.AddField(
            model_name='about',
            name='mission_phrase',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='about',
            name='right_believe_phrase',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
        migrations.AddField(
            model_name='about',
            name='rotating_list',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='about',
            name='some_phrase',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='about',
            name='some_phrase_author',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='about',
            name='vision_image',
            field=models.ImageField(default='fab_hose_africa_web/no_image.png', upload_to='fab_hose_africa_web/about'),
        ),
        migrations.AddField(
            model_name='about',
            name='vision_phrase',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]