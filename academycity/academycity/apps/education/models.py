from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class InstitutionWeb(models.Model):

    class Meta:
        verbose_name = _('institution')
        verbose_name_plural = _('institutions')
        ordering = ['order']

    order = models.IntegerField(default=1000, null=True, blank=True)
    institution_name = models.CharField(max_length=100, null=True, blank=True)
    domain_name = models.CharField(max_length=100, null=True, blank=True)
    welcome_phrase = models.CharField(max_length=100, null=True, blank=True)
    institution_image = models.ImageField(upload_to='institution/', blank=True, null=True)
    logo_image = models.ImageField(upload_to='institution/', blank=True, null=True)
    footer_image = models.ImageField(upload_to='institution/', blank=True, null=True)

    institution_short_description = models.CharField(max_length=200, null=True, blank=True)
    youtube_video_address = models.CharField(max_length=100, null=True)

    address1 = models.CharField(max_length=100, null=True, blank=True)
    address2 = models.CharField(max_length=100, null=True, blank=True)

    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return self.institution_name


class Course(models.Model):

    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')
        ordering = ['order']

    institution_web = models.ForeignKey(InstitutionWeb, on_delete=models.CASCADE, default=1, related_name='courses')
    order = models.IntegerField(default=1000, blank=True)
    course_name = models.CharField(max_length=100, null=True)
    course_description = models.CharField(max_length=200, null=True)
    course_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    is_popular = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)


class New(models.Model):

    class Meta:
        verbose_name = _('news')
        verbose_name_plural = _('news')
        ordering = ['order']

    institution_web = models.ForeignKey(InstitutionWeb, on_delete=models.CASCADE,  default=1, related_name='news')
    order = models.IntegerField(default=1000, blank=True)
    news_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    news_type = models.CharField(max_length=100, null=True)
    news_type_description = models.CharField(max_length=100, null=True)
    news_title = models.CharField(max_length=100, null=True)
    news_description = models.CharField(max_length=500, null=True)
    is_popular = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)


class Program(models.Model):

    class Meta:
        verbose_name = _('Program')
        verbose_name_plural = _('Programs')
        ordering = ['order']

    institution_web = models.ForeignKey(InstitutionWeb, on_delete=models.CASCADE,  default=1, related_name='programs')
    order = models.IntegerField(default=1000, blank=True)
    image = models.ImageField(upload_to='Programs/', blank=True, null=True)
    program_title = models.CharField(max_length=100, null=True)
    program_description = models.CharField(max_length=500, null=True)
    is_popular = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)


class Subject(models.Model):

    class Meta:
        verbose_name = _('subject')
        verbose_name_plural = _('subjects')
        ordering = ['order']

    institution_web = models.ForeignKey(InstitutionWeb, on_delete=models.CASCADE, default=1, related_name='subjects')
    order = models.IntegerField(default=1000, blank=True)
    image = models.ImageField(upload_to='subjects/', blank=True, null=True)
    subject_name = models.CharField(max_length=100, null=True)
    is_popular = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)


class Person(models.Model):

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        ordering = ['order']

    institution_web = models.ForeignKey(InstitutionWeb, on_delete=models.CASCADE, default=1, related_name='persons')
    order = models.IntegerField(default=1000, blank=True)
    image = models.ImageField(upload_to='person/', blank=True, null=True)
    persons_name = models.CharField(max_length=100, null=True)
    persons_duty = models.CharField(max_length=100, null=True)
    persons_description = models.CharField(max_length=500, null=True)
    is_popular = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)


class Phrase(models.Model):

    class Meta:
        verbose_name = _('phrase')
        verbose_name_plural = _('phrases')
        ordering = ['order']

    institution_web = models.ForeignKey(InstitutionWeb, on_delete=models.CASCADE, default=1, related_name='phrases')
    order = models.IntegerField(default=1000, blank=True)
    image = models.ImageField(upload_to='phrase/', blank=True, null=True)
    persons_phrase = models.CharField(max_length=500, null=True)
    is_active = models.BooleanField(default=True)


class AdditionalTopic(models.Model):

    class Meta:
        verbose_name = _('topic')
        verbose_name_plural = _('topics')
        ordering = ['order']

    institution_web = models.ForeignKey(InstitutionWeb, on_delete=models.CASCADE, default=1, related_name='topics')
    order = models.IntegerField(default=1000, blank=True)
    image = models.ImageField(upload_to='phrase/', blank=True, null=True)
    topic_description = models.CharField(max_length=500, null=True)
    is_active = models.BooleanField(default=True)

