# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from cms.admin.placeholderadmin import PlaceholderAdminMixin
from parler.admin import TranslatableAdmin

from .models import (Category, Product)


class CategoryAdmin(TranslatableAdmin, PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('language_column', 'name', )
    fieldsets = (
        (None, {
         'fields': (
            'image',
            'order',
         )
        }),
        (_('Translated Fields'), {
            'fields': (
                'name',
                'slug',
            ),
        }),
    )

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


# ---
class ProductAdmin(TranslatableAdmin, PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('language_column', 'name', 'category', )
    fieldsets = (
        (None, {
            'fields': (
                'image', 'category', 'order', 'price',
            )
        }),
        (_('Translated Fields'), {
            'fields': (
                'name',
                'slug',
            ),
        }),
    )

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
