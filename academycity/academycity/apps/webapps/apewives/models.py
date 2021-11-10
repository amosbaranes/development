from django.db import models


class ApewivesWeb(models.Model):

    company_name = models.CharField(max_length=100, null=True)
    main_page_image = models.ImageField(upload_to="apewives_web/home", default="apewives_web/home/no_image.png")
    text_main_page_title = models.CharField(max_length=100, default='', blank=True)

    text_second_page_title = models.CharField(max_length=256, default='', blank=True)
    text_second_page_text = models.CharField(max_length=512, default='', blank=True)

    membership_image = models.ImageField(upload_to="apewives_web/home", default="apewives_web/home/no_image.png")
    membership_title = models.CharField(max_length=100, default='', blank=True)
    membership_text = models.CharField(max_length=512, default='', blank=True)

    specs_image = models.ImageField(upload_to="apewives_web/home", default="apewives_web/home/no_image.png")
    specs_title = models.CharField(max_length=100, default='', blank=True)
    specs_text = models.CharField(max_length=512, default='', blank=True)

    ownership_image = models.ImageField(upload_to="apewives_web/home", default="apewives_web/home/no_image.png")

    roadmap_image = models.ImageField(upload_to="apewives_web/home", default="apewives_web/home/no_image.png")

    def __str__(self):
        return self.company_name


class TitleSlides(models.Model):

    class Meta:
        verbose_name = 'title slide'
        verbose_name_plural = 'title slides'
        ordering = ['order']

    order = models.PositiveSmallIntegerField(default=0)
    apewives = models.ForeignKey(ApewivesWeb, null=True, on_delete=models.CASCADE, related_name='titleslides')
    text = models.CharField(max_length=512, default='', blank=True)


class SlidingImages(models.Model):

    class Meta:
        verbose_name = 'sliding image'
        verbose_name_plural = 'sliding images'
        ordering = ['order']

    order = models.PositiveSmallIntegerField(default=0)
    apewives = models.ForeignKey(ApewivesWeb, null=True, on_delete=models.CASCADE, related_name='sliding_images')
    image = models.ImageField(upload_to="apewives_web/home", default="apewives_web/home/no_image.png")


class Roadmap(models.Model):

    class Meta:
        verbose_name = 'roadmap'
        verbose_name_plural = 'roadmaps'
        ordering = ['order']

    order = models.PositiveSmallIntegerField(default=0)
    apewives = models.ForeignKey(ApewivesWeb, null=True, on_delete=models.CASCADE, related_name='roadmaps')
    text = models.CharField(max_length=512, default='', blank=True)
    link = models.CharField(max_length=100, default='', blank=True)


class Team(models.Model):

    class Meta:
        verbose_name = 'team'
        verbose_name_plural = 'teams'
        ordering = ['order']

    order = models.PositiveSmallIntegerField(default=0)
    apewives = models.ForeignKey(ApewivesWeb, null=True, on_delete=models.CASCADE, related_name='teams')
    image = models.ImageField(upload_to="apewives_web/team", default="apewives_web/home/no_image.png")

