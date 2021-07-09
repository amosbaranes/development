from django.db import models
from filer.fields.image import FilerImageField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse


class FabHoseAfricaWeb(models.Model):

    class Meta:
        verbose_name = 'fab_hose_africa_web'
        verbose_name_plural = 'fab_hose_africa_webs'

    company_name = models.CharField(max_length=200, default='', blank=True)
    image_logo = models.ImageField(upload_to="fab_hose_africa_web", default="fab_hose_africa_web/no_image.png")

    office_address_1 = models.CharField(max_length=100, default='', blank=True)
    office_address_2 = models.CharField(max_length=100, default='', blank=True)
    opening_hours_1 = models.CharField(max_length=100, default='', blank=True)
    opening_hours_2 = models.CharField(max_length=100, default='', blank=True)
    call_1 = models.CharField(max_length=100, default='', blank=True)
    call_2 = models.CharField(max_length=100, default='', blank=True)
    email_sale_1 = models.CharField(max_length=100, default='', blank=True)
    email_sale_2 = models.CharField(max_length=100, default='', blank=True)
    email_inquire_1 = models.CharField(max_length=100, default='', blank=True)
    email_inquire_2 = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return self.company_name


class Home(models.Model):

    class Meta:
        verbose_name = 'home'
        verbose_name_plural = 'homes'

    fab_hose_africa_web = models.OneToOneField(FabHoseAfricaWeb, null=True,
                                               on_delete=models.CASCADE, related_name='home')
    background_map = models.ImageField(upload_to="fab_hose_africa_web/home",
                                       default="fab_hose_africa_web/no_image.png")
    image_moving = models.ImageField(upload_to="fab_hose_africa_web/home",
                                     default="fab_hose_africa_web/no_image.png")

    background_1 = models.ImageField(upload_to="fab_hose_africa_web/home", default="fab_hose_africa_web/no_image.png")
    background_2 = models.ImageField(upload_to="fab_hose_africa_web/home", default="fab_hose_africa_web/no_image.png")
    right_image = models.ImageField(upload_to="fab_hose_africa_web/home", default="fab_hose_africa_web/no_image.png")
    left_image = models.ImageField(upload_to="fab_hose_africa_web/home", default="fab_hose_africa_web/no_image.png")

    title = models.CharField(max_length=100, default='', blank=True)
    rotating_list = models.CharField(max_length=500, default='', blank=True)
    contact_phrase = models.CharField(max_length=500, default='', blank=True)

    counter_1_title = models.CharField(max_length=20, default='', blank=True)
    counter_1_count = models.PositiveSmallIntegerField(default=1, blank=True)
    counter_2_title = models.CharField(max_length=20, default='', blank=True)
    counter_2_count = models.PositiveSmallIntegerField(default=2, blank=True)
    counter_3_title = models.CharField(max_length=20, default='', blank=True)
    counter_3_count = models.PositiveSmallIntegerField(default=8, blank=True)
    counter_4_title = models.CharField(max_length=20, default='', blank=True)
    counter_4_count = models.PositiveSmallIntegerField(default=600, blank=True)

    little_about_us = models.CharField(max_length=500, default='', blank=True)
    about_our_products = models.CharField(max_length=500, default='', blank=True)

    def __str__(self):
        return str(self.fab_hose_africa_web.company_name) + ' ' + str(self.title)


class Catalog(models.Model):

    class Meta:
        verbose_name = 'catalog'
        verbose_name_plural = 'catalogs'

    fab_hose_africa_web = models.OneToOneField(FabHoseAfricaWeb, null=True,
                                               on_delete=models.CASCADE, related_name='catalog')
    background_title_image = models.ImageField(upload_to="fab_hose_africa_web/catalog",
                                               default="fab_hose_africa_web/no_image.png")
    title = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return str(self.fab_hose_africa_web.company_name) + ': ' + str(self.title)


class CatalogSection(models.Model):

    class Meta:
        verbose_name = 'catalog section'
        verbose_name_plural = 'catalog sections'
        ordering = ['id']

    category = models.ForeignKey(Catalog, null=True, on_delete=models.CASCADE, related_name='sections')
    background_image = models.ImageField(upload_to="fab_hose_africa_web/catalog/section", default="fab_hose_africa_web/no_image.png")
    section_title = models.CharField(max_length=100, default='', blank=True)
    section_description = models.CharField(max_length=1000, default='', blank=True)

    def __str__(self):
        return self.section_title


class CatalogSectionCategory(models.Model):

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    section = models.ForeignKey(CatalogSection, null=True, on_delete=models.CASCADE, related_name='categories')
    category_title = models.CharField(max_length=100, default='', blank=True)
    category_link = models.CharField(max_length=100, default='', blank=True)
    category_image = models.ImageField(upload_to="fab_hose_africa_web/catalog/section/category",
                                       default="fab_hose_africa_web/no_image.png")
    category_description = models.CharField(max_length=1000, default='', blank=True)
    category_id = models.PositiveIntegerField(default=1)
    data_date = models.CharField(max_length=20, default='')
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('fabhouseafrica:category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.category_title


class CatalogSectionCategoryStyle(models.Model):

    class Meta:
        verbose_name = 'Style'
        verbose_name_plural = 'Styles'

    category = models.ForeignKey(CatalogSectionCategory, null=True, on_delete=models.CASCADE,
                                 related_name='category_styles')
    style_title = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return str(self.category.category_title) + ': ' + str(self.style_title)


class CatalogSectionImageStyleImage(models.Model):
    class Meta:
        verbose_name = 'style_image'
        verbose_name_plural = 'style_images'

    style = models.ForeignKey(CatalogSectionCategoryStyle, null=True, on_delete=models.CASCADE,
                              related_name='style_images')
    image_title = models.CharField(max_length=100, default='', blank=True)
    image = models.ImageField(upload_to="fab_hose_africa_web/catalog/section/category/style",
                              default="fab_hose_africa_web/no_image.png")

    def __str__(self):
        return str(self.style.style_title) + ': ' + str(self.image_title)


class About(models.Model):

    class Meta:
        verbose_name = 'about'
        verbose_name_plural = 'abouts'

    fab_hose_africa_web = models.OneToOneField(FabHoseAfricaWeb, null=True,
                                               on_delete=models.CASCADE, related_name='about')
    about_us_title = models.CharField(max_length=100, default='', blank=True)
    about_us_image = models.ImageField(upload_to="fab_hose_africa_web/about",
                                       default="fab_hose_africa_web/no_image.png")

    believe_phrase = models.CharField(max_length=200, default='', blank=True)
    rotating_list = models.CharField(max_length=500, default='', blank=True)
    believe_image = models.ImageField(upload_to="fab_hose_africa_web/about/believe",
                                      default="fab_hose_africa_web/no_image.png")
    left_believe_phrase = models.CharField(max_length=250, default='', blank=True)
    Fabulous_title = models.CharField(max_length=100, default='', blank=True)
    right_believe_phrase = models.CharField(max_length=250, default='', blank=True)

    company_history_image_left = models.ImageField(upload_to="fab_hose_africa_web/about/history",
                                                   default="fab_hose_africa_web/no_image.png")
    company_history_image_right = models.ImageField(upload_to="fab_hose_africa_web/about/history",
                                                    default="fab_hose_africa_web/no_image.png")
    company_legacy = models.CharField(max_length=1000, default='', blank=True)
    company_history = models.CharField(max_length=1000, default='', blank=True)
    some_phrase = models.CharField(max_length=100, default='', blank=True)
    some_phrase_author = models.CharField(max_length=50, default='', blank=True)

    background_image = models.ImageField(upload_to="fab_hose_africa_web/about",
                                         default="fab_hose_africa_web/no_image.png")
    mission_image = models.ImageField(upload_to="fab_hose_africa_web/about",
                                      default="fab_hose_africa_web/no_image.png")
    vision_image = models.ImageField(upload_to="fab_hose_africa_web/about",
                                     default="fab_hose_africa_web/no_image.png")
    mission_phrase = models.CharField(max_length=500, default='', blank=True)
    vision_phrase = models.CharField(max_length=500, default='', blank=True)


class Contact(models.Model):

    class Meta:
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'

    fab_hose_africa_web = models.OneToOneField(FabHoseAfricaWeb, null=True,
                                               on_delete=models.CASCADE, related_name='contact')

    background_title_image = models.ImageField(upload_to="fab_hose_africa_web/contact",
                                               default="fab_hose_africa_web/no_image.png")
    background_1 = models.ImageField(upload_to="fab_hose_africa_web/contact", default="fab_hose_africa_web/no_image.png")
    title = models.CharField(max_length=100, default='', blank=True)

    information_title = models.CharField(max_length=100, default='', blank=True)
    send_message_title = models.CharField(max_length=100, default='', blank=True)
    contact_us_email = models.CharField(max_length=50, default='', blank=True)

    def __str__(self):
        return str(self.fab_hose_africa_web.company_name)


class ReceivedMessages(models.Model):
    class Meta:
        verbose_name = 'received_message'
        verbose_name_plural = 'received_messages'

    contact = models.ForeignKey(Contact, null=True, on_delete=models.CASCADE, related_name='received_messages')
    name = models.CharField(max_length=100, default='', blank=True)
    email = models.CharField(max_length=100, default='', blank=True)
    subject = models.CharField(max_length=100, default='', blank=True)
    message = models.CharField(max_length=2000, default='', blank=True)


class ContactInformation(models.Model):
    class Meta:
        verbose_name = 'contact information'
        verbose_name_plural = 'contact information'

    contact = models.ForeignKey(Contact, null=True, on_delete=models.CASCADE, related_name='information')
    title = models.CharField(max_length=100, default='', blank=True)
    description = models.CharField(max_length=1000, default='', blank=True)


class Gallery(models.Model):

    class Meta:
        verbose_name = 'gallery'
        verbose_name_plural = 'galleries'

    fab_hose_africa_web = models.OneToOneField(FabHoseAfricaWeb, null=True,
                                               on_delete=models.CASCADE, related_name='gallery')
    title = models.CharField(max_length=100, default='', blank=True)
    background_title_image = models.ImageField(upload_to="fab_hose_africa_web/gallery",
                                               default="fab_hose_africa_web/no_image.png")
    section_title = models.CharField(max_length=100, default='', blank=True)
    section_background_title_image = models.ImageField(upload_to="fab_hose_africa_web/gallery",
                                                       default="fab_hose_africa_web/no_image.png")

    def __str__(self):
        return str(self.fab_hose_africa_web.company_name) + ' ' + str(self.title)


class GalleryItems(models.Model):

    class Meta:
        verbose_name = 'gallery item'
        verbose_name_plural = 'gallery items'
        ordering = ['-image_title',]

    gallery = models.ForeignKey(Gallery, null=True, on_delete=models.CASCADE, related_name='gallery_items')
    image_title = models.CharField(max_length=100, default='', blank=True)
    image = models.ImageField(upload_to="fab_hose_africa_web/gallery/items",
                              default="fab_hose_africa_web/no_image.png")

    def __str__(self):
        return self.image_title

