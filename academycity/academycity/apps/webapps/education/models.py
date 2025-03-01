from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from cms.models.fields import PlaceholderField
from ...courses.models import Course


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

    institute_name_color = models.CharField(max_length=100, default='black', null=True, blank=True)
    introduction_phrase_color = models.CharField(max_length=100, default='black', null=True, blank=True)
    searching_title = models.CharField(max_length=100, null=True, blank=True)
    search_explore_catalog_title = models.CharField(max_length=100, null=True, blank=True)

    logo_image = models.ImageField(upload_to='institution/', blank=True, null=True)
    footer_image = models.ImageField(upload_to='institution/', blank=True, null=True)
    contact_us_image = models.ImageField(upload_to='institution/', blank=True, null=True)
    footer_phrase = models.CharField(max_length=100, null=True, blank=True)
    institution_short_description = models.CharField(max_length=200, null=True, blank=True)
    youtube_video_address = models.CharField(max_length=100, null=True)

    address1 = models.CharField(max_length=100, null=True, blank=True)
    address2 = models.CharField(max_length=100, null=True, blank=True)

    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=40, null=True, blank=True)

    programs_title = models.CharField(max_length=100, null=True, blank=True)
    courses_title = models.CharField(max_length=100, null=True, blank=True)
    services_title = models.CharField(max_length=100, null=True, blank=True)
    new_title = models.CharField(max_length=100, null=True, blank=True)
    subjects_title = models.CharField(max_length=100, null=True, blank=True)
    person_title = models.CharField(max_length=100, null=True, blank=True)
    person_phrase_title = models.CharField(max_length=100, null=True, blank=True)
    other_title = models.CharField(max_length=100, null=True, blank=True)

    facebook_link = models.CharField(max_length=100, null=True, blank=True)
    linkedin_link = models.CharField(max_length=100, null=True, blank=True)
    twitter_link = models.CharField(max_length=100, null=True, blank=True)
    instagram_link = models.CharField(max_length=100, null=True, blank=True)
    github_link = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.institution_name


class ReceivedMessages(models.Model):
    class Meta:
        verbose_name = _('received_message')
        verbose_name_plural = _('received_messages')

    institution_web = models.ForeignKey(InstitutionWeb, on_delete=models.CASCADE, default=1,
                                        related_name='received_messages')
    name = models.CharField(max_length=100, default='', blank=True)
    email = models.CharField(max_length=100, default='', blank=True)
    subject = models.CharField(max_length=100, default='', blank=True)
    message = models.CharField(max_length=2000, default='', blank=True)


class Course(models.Model):

    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')
        ordering = ['order']

    institution_web = models.ForeignKey(InstitutionWeb, on_delete=models.CASCADE, default=1, related_name='courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=21, related_name='course_courses')
    order = models.IntegerField(default=1000, blank=True)
    name = models.CharField(max_length=100, null=True)
    date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    is_popular = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    short_description = models.CharField(max_length=200, null=True)
    description = PlaceholderField('description', related_name='education_course_description')
    name_text_color = models.CharField(max_length=30, default='#090909',null=True)
    name_gradient_deg = models.IntegerField(default=285, blank=True)
    gradient_color_1 = models.CharField(max_length=30, default='#969696',null=True)
    gradient_color_2 = models.CharField(max_length=30, default='#dfdfdf',null=True)


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
    description = PlaceholderField('description', related_name='new_description')
    name_text_color = models.CharField(max_length=30, default='#090909', null=True)
    name_gradient_deg = models.IntegerField(default=285, blank=True)
    gradient_color_1 = models.CharField(max_length=30, default='#969696', null=True)
    gradient_color_2 = models.CharField(max_length=30, default='#dfdfdf', null=True)
    is_links = models.BooleanField(default=True)


class Program(models.Model):

    class Meta:
        verbose_name = _('Program')
        verbose_name_plural = _('Programs')
        ordering = ['order']

    institution_web = models.ForeignKey(InstitutionWeb, on_delete=models.CASCADE,  default=1, related_name='programs')
    order = models.IntegerField(default=1000, blank=True)
    image = models.ImageField(upload_to='Programs/', blank=True, null=True)
    name = models.CharField(max_length=100, null=True)
    short_description = models.CharField(max_length=500, null=True)
    is_popular = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    description = PlaceholderField('description', related_name='program_description')
    name_text_color = models.CharField(max_length=30, default='#090909',null=True)
    name_gradient_deg = models.IntegerField(default=285, blank=True)
    gradient_color_1 = models.CharField(max_length=30, default='#969696',null=True)
    gradient_color_2 = models.CharField(max_length=30, default='#dfdfdf',null=True)


class Services(models.Model):

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ['order']

    institution_web = models.ForeignKey(InstitutionWeb, on_delete=models.CASCADE,  default=1, related_name='services')
    order = models.IntegerField(default=1000, blank=True)
    image = models.ImageField(upload_to='Programs/', blank=True, null=True)
    name = models.CharField(max_length=100, null=True)
    short_description = models.CharField(max_length=500, null=True)
    is_active = models.BooleanField(default=True)
    description = PlaceholderField('description', related_name='service_description')
    name_text_color = models.CharField(max_length=30, default='#090909', null=True)
    name_gradient_deg = models.IntegerField(default=285, blank=True)
    gradient_color_1 = models.CharField(max_length=30, default='#969696', null=True)
    gradient_color_2 = models.CharField(max_length=30, default='#dfdfdf', null=True)


class Subject(models.Model):

    class Meta:
        verbose_name = _('subject')
        verbose_name_plural = _('subjects')
        ordering = ['order']

    institution_web = models.ForeignKey(InstitutionWeb, on_delete=models.CASCADE, default=1, related_name='subjects')
    order = models.IntegerField(default=1000, blank=True)
    image = models.ImageField(upload_to='subjects/', blank=True, null=True)
    name = models.CharField(max_length=100, null=True)
    is_popular = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    description = PlaceholderField('description', related_name='subject_description')
    name_text_color = models.CharField(max_length=30, default='#090909', null=True)
    name_gradient_deg = models.IntegerField(default=285, blank=True)
    gradient_color_1 = models.CharField(max_length=30, default='#969696', null=True)
    gradient_color_2 = models.CharField(max_length=30, default='#dfdfdf', null=True)


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
    description = PlaceholderField('description', related_name='person_description')
    cv_type = models.CharField(max_length=15, null=True, default='')
    cv_number = models.SmallIntegerField(default=1)


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
    topic_name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_links = models.BooleanField(default=True)
    description = PlaceholderField('description', related_name='topic_description')


class MoreNewsDetail(models.Model):

    class Meta:
        verbose_name = _('more_news_detail')
        verbose_name_plural = _('more_news_details')
        ordering = ['order']

    institution_web = models.ForeignKey(InstitutionWeb, on_delete=models.CASCADE,  default=1, related_name=
                                        'more_news_details')
    order = models.IntegerField(default=1000, blank=True)
    news_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='news_detail/', blank=True, null=True)
    news_type = models.CharField(max_length=100, null=True)
    news_type_description = models.CharField(max_length=100, null=True)
    news_title = models.CharField(max_length=100, null=True)
    news_description = models.CharField(max_length=500, null=True)
    is_popular = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

