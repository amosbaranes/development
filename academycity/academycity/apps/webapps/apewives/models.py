from django.db import models


class ApewivesWeb(models.Model):
    company_name = models.CharField(max_length=100, null=True)
    main_page_image = models.ImageField(upload_to="apewives_web/home/main_page_image", default="no_image.png")
    main_page_twitter_image = models.ImageField(upload_to="apewives_web/home/social_media_images", default="no_image.png")
    main_page_twitter_link = models.CharField(max_length=100, default='')
    main_page_discord_image = models.ImageField(upload_to="apewives_web/home/social_media_images", default="no_image.png")
    main_page_discord_link = models.CharField(max_length=100, default='')
    main_page_logo_image = models.ImageField(upload_to="apewives_web/home/main_page_image", default="no_image.png")
    text_main_page_title = models.CharField(max_length=100, default='')

    text_second_page_title = models.CharField(max_length=256, default='')
    text_second_page_text = models.TextField(blank=True, null=True)

    apes_out_title = models.CharField(max_length=256, default='')
    apes_out_text = models.TextField(blank=True, null=True)

    # comics bridge
    specs_image = models.ImageField(upload_to="apewives_web/home/specs_images", default="no_image.png")
    specs_title = models.CharField(max_length=100, default='')
    specs_text_paragraph = models.TextField(blank=True, null=True)

    # Meta Universe
    ownership_image = models.ImageField(upload_to="apewives_web/home/ownership_images", default="no_image.png")
    ownership_title = models.CharField(max_length=100, default='')
    ownership_text_paragraph = models.TextField(blank=True, null=True)

    roadmap_image = models.ImageField(upload_to="apewives_web/home/roadmap_images", default="no_image.png")
    roadmap_title = models.CharField(max_length=100, default='')

    team_title = models.CharField(max_length=100, default='')
    team_text = models.TextField(blank=True, null=True)

    footer_desc = models.CharField(max_length=100, default='')

    youtube_image = models.ImageField(upload_to="apewives_web/home/social_media_images", default="no_image.png")
    youtube_link = models.CharField(max_length=100, default='')
    instagram_image = models.ImageField(upload_to="apewives_web/home/social_media_images", default="no_image.png")
    instagram_link = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.company_name


class TitleSlides(models.Model):

    class Meta:
        verbose_name = 'title slide'
        verbose_name_plural = 'title slides'
        ordering = ['order']

    order = models.PositiveSmallIntegerField(default=0)
    apewives = models.ForeignKey(ApewivesWeb, null=True, on_delete=models.CASCADE, related_name='titleslides')
    text = models.TextField(blank=True, null=True)


class SlidingImages(models.Model):

    class Meta:
        verbose_name = 'sliding image'
        verbose_name_plural = 'sliding images'
        ordering = ['order']

    order = models.PositiveSmallIntegerField(default=0)
    apewives = models.ForeignKey(ApewivesWeb, null=True, on_delete=models.CASCADE, related_name='sliding_images')
    image = models.ImageField(upload_to="apewives_web/home/sliding_images",
                              default="apewives_web/home/no_image.png")


class Roadmap(models.Model):

    class Meta:
        verbose_name = 'roadmap'
        verbose_name_plural = 'roadmaps'
        ordering = ['order']

    order = models.PositiveSmallIntegerField(default=0)
    apewives = models.ForeignKey(ApewivesWeb, null=True, on_delete=models.CASCADE, related_name='roadmaps')
    text = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=100, null=True, blank=True)
    link_name = models.CharField(max_length=100, default='', blank=True)
    roadmap_data_id = models.CharField(max_length=100, default='', blank=True)
    roadmap_timeline_item_point = models.IntegerField(default=10)


class Team(models.Model):

    class Meta:
        verbose_name = 'team'
        verbose_name_plural = 'teams'
        ordering = ['order']

    order = models.PositiveSmallIntegerField(default=0)
    apewives = models.ForeignKey(ApewivesWeb, null=True, on_delete=models.CASCADE, related_name='teams')
    image = models.ImageField(upload_to="apewives_web/team/team_images", default="apewives_web/home/no_image.png")
    team_header = models.CharField(max_length=100, default='', blank=True)
    team_description = models.CharField(max_length=512, default='', blank=True)
    data_id_1 = models.CharField(max_length=25, default='', blank=True)
    data_id_2 = models.CharField(max_length=25, default='', blank=True)

