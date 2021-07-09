from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from cms.models.fields import PlaceholderField


class CheckCashingWeb(models.Model):

    class Meta:
        verbose_name = _('check cashing')
        verbose_name_plural = _('check cashing')
        ordering = ['order']

    order = models.IntegerField(default=1000, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    domain_name = models.CharField(max_length=100, null=True, blank=True)
    main_image = models.ImageField(upload_to='checkcashing/', blank=True, null=True)
    logo_image = models.ImageField(upload_to='checkcashing/', blank=True, null=True)
    background_location_image = models.ImageField(upload_to='location/', blank=True, null=True)
    background_currency_image = models.ImageField(upload_to='currency/', blank=True, null=True)
    main_title = models.CharField(max_length=100, null=True)
    footer_main_title = models.CharField(max_length=100, null=True)
    main_sub_title = models.CharField(max_length=100, null=True)
    location_title = models.CharField(max_length=100, null=True)
    partner_title = models.CharField(max_length=100, null=True)
    main_sub_description = models.CharField(max_length=500, null=True)
    check_cashing_application = models.FileField(upload_to='checkcashing/', blank=True, null=True)
    application_for_employment = models.FileField(upload_to='checkcashing/', blank=True, null=True)
    copy_right_year = models.CharField(max_length=4, null=True)
    contact_us_email = models.CharField(max_length=100, null=True)
    members_password = models.CharField(max_length=100, default='101')

    def __str__(self):
        return self.name


class LocationRegion(models.Model):

    class Meta:
        verbose_name = _('location_region')
        verbose_name_plural = _('location_regions')
        ordering = ['order']

    check_cashing_web = models.ForeignKey(CheckCashingWeb, on_delete=models.CASCADE, related_name='location_regions')
    order = models.IntegerField(default=1000, blank=True)
    region_title = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=250, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.region_title)
        super(LocationRegion, self).save(*args, **kwargs)

    def __str__(self):
        return self.region_title


class Location(models.Model):

    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')
        ordering = ['order']

    check_cashing_web = models.ForeignKey(CheckCashingWeb, on_delete=models.CASCADE,
                                          related_name='locations')
    region = models.ForeignKey(LocationRegion, on_delete=models.CASCADE, blank=True, null=True,
                               related_name='region_locations')
    order = models.IntegerField(default=1000, blank=True)
    image = models.ImageField(upload_to='location/', blank=True, null=True)
    location_heading = models.CharField(max_length=100, null=True)
    location_detail_title = models.CharField(max_length=100, null=True)
    address1 = models.CharField(max_length=50, null=True)
    address2 = models.CharField(max_length=50, null=True)
    address3 = models.CharField(max_length=50, null=True)
    address4 = models.CharField(max_length=50, null=True)
    working_hours1 = models.CharField(max_length=50, blank=True, null=True)
    working_hours2 = models.CharField(max_length=50, blank=True, null=True)
    working_hours3 = models.CharField(max_length=50, blank=True, null=True)
    working_hours4 = models.CharField(max_length=50, blank=True, null=True)
    data_ajax_id = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=250, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.location_heading)
        super(Location, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('checkcashingchicago:location_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.location_heading


class Service(models.Model):

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')
        ordering = ['order']

    location = models.ManyToManyField(Location, related_name='services')
    order = models.IntegerField(default=1000, blank=True)
    title = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=800, null=True)


class Currency(models.Model):

    class Meta:
        verbose_name = _('currency')
        verbose_name_plural = _('currencies')
        ordering = ['order']

    check_cashing_web = models.ForeignKey(CheckCashingWeb, on_delete=models.CASCADE, default=1,
                                          related_name='currencies')
    order = models.IntegerField(default=1000, blank=True)
    image = models.ImageField(upload_to='currency/', blank=True, null=True)
    currency_header = models.CharField(max_length=100, null=True)
    currency_description = models.CharField(max_length=500, null=True)
    image_id = models.IntegerField(default=0)
    currency_loop = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)


class Partner(models.Model):

    class Meta:
        verbose_name = _('partner')
        verbose_name_plural = _('partners')
        ordering = ['order']

    check_cashing_web = models.ForeignKey(CheckCashingWeb, on_delete=models.CASCADE, default=1,
                                          related_name='partners')
    order = models.IntegerField(default=1000, blank=True)
    partner_image = models.ImageField(upload_to='partner/', blank=True, null=True)
    partner_description = models.CharField(max_length=100, null=True)
    partner_link = models.CharField(max_length=100, null=True)
    image_id = models.IntegerField(default=0)
    image_width = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)


class ContactUsMessages(models.Model):

    class Meta:
        verbose_name = _('contact_us_message')
        verbose_name_plural = _('contact_us_messages')

    check_cashing_web = models.ForeignKey(CheckCashingWeb, on_delete=models.CASCADE, default=1,
                                          related_name='messages')

    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    message = models.TextField(null=True)


class DocumentCategory(models.Model):

    class Meta:
        verbose_name = _('document_category')
        verbose_name_plural = _('document_categories')

    check_cashing_web = models.ForeignKey(CheckCashingWeb, on_delete=models.CASCADE, default=1,
                                          related_name='document_categories')
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Document(models.Model):

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')

    category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE, default=1,
                                 related_name='category_documents')
    name = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to='checkcashing/documents', blank=True, null=True)

    def __str__(self):
        return self.name
