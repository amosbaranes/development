# Generated by Django 3.1.13 on 2021-11-17 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apewives', '0035_auto_20211117_0527'),
    ]

    operations = [
        migrations.AddField(
            model_name='apewivesweb',
            name='about_text_bottom',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='about_text_top',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='buy_image',
            field=models.ImageField(default='no_image.png', upload_to='apewives_web/home/buy_images'),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='community_discord_image',
            field=models.ImageField(default='no_image.png', upload_to='apewives_web/home/social_media_images'),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='community_twitter_image',
            field=models.ImageField(default='no_image.png', upload_to='apewives_web/home/social_media_images'),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='contract_address_text_paragraph',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='instagram_image',
            field=models.ImageField(default='no_image.png', upload_to='apewives_web/home/social_media_images'),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='main_page_discord_image',
            field=models.ImageField(default='no_image.png', upload_to='apewives_web/home/social_media_images'),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='main_page_logo_image',
            field=models.ImageField(default='no_image.png', upload_to='apewives_web/home/main_page_image'),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='main_page_twitter_image',
            field=models.ImageField(default='no_image.png', upload_to='apewives_web/home/social_media_images'),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='main_page_twitter_link',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='membership_image',
            field=models.ImageField(default='no_image.png', upload_to='apewives_web/home/membership_images'),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='ownership_image',
            field=models.ImageField(default='no_image.png', upload_to='apewives_web/home/ownership_images'),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='ownership_text_paragraph',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='roadmap_image',
            field=models.ImageField(default='no_image.png', upload_to='apewives_web/home/roadmap_images'),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='specs_image',
            field=models.ImageField(default='no_image.png', upload_to='apewives_web/home/specs_images'),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='specs_text_paragraph',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='text_main_page_title',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='apewivesweb',
            name='youtube_image',
            field=models.ImageField(default='no_image.png', upload_to='apewives_web/home/social_media_images'),
        ),
        migrations.AlterField(
            model_name='apewivesweb',
            name='company_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
