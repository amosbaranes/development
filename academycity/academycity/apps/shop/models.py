# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.db import models
from django.utils.text import slugify
# from django.utils.encoding import python_2_unicode_compatible, force_text
from django.utils.translation import ugettext_lazy as _, get_language

from filer.fields.image import FilerImageField
from cms.models.fields import PlaceholderField
from parler.models import TranslatableModel, TranslatedFields
from parler.utils.context import switch_language
from ..core.fields import OrderField


# @python_2_unicode_compatible
class Category(TranslatableModel):
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    description = PlaceholderField('category_description')
    image = FilerImageField(blank=True, null=True, on_delete=models.SET_NULL)
    order = OrderField(blank=True, for_fields=[], default=1)

    translations = TranslatedFields(
        name=models.CharField(_('name'), blank=False, default='', db_index=True,
                              help_text=_('Please supply the category name.'), max_length=128),
        slug=models.SlugField(_('slug'), blank=False, default='', db_index=True,
                              help_text=_('Please supply the category slug.'), max_length=128)
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify('category-' + self.name + ' ' + get_language())
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        with switch_language(self, get_language()):
            return reverse('shop:product_list_by_category', args=[self.slug])

    def __str__(self):
        return str(self.order) + ". "+ self.name


# @python_2_unicode_compatible
class Product(TranslatableModel):
    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    description = PlaceholderField('product_description')
    image = FilerImageField(blank=True, null=True, on_delete=models.SET_NULL, related_name='product_image')
    order = OrderField(blank=True, for_fields=[], default=1)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    translations = TranslatedFields(
        name=models.CharField(_('name'), blank=False, default='', db_index=True,
                              help_text=_('Please supply the product name.'), max_length=128),
        slug=models.SlugField(_('slug'), blank=False, default='', db_index=True,
                              help_text=_('Please supply the product slug.'), max_length=128)
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify('product-' + self.name + ' ' + get_language())
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        with switch_language(self, get_language()):
            return reverse('shop:product_detail', kwargs={'slug': self.slug, })

    def __str__(self):
        return str(self.order) + ". "+ self.name



