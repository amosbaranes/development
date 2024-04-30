from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (StockPricesDays, CompanyInfo)


# -*- coding: utf-8 -*-
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from parler.admin import TranslatableAdmin, TranslatableStackedInline, TranslatableTabularInline


@admin.register(CompanyInfo)
class XBRLCompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticker', 'company_name')
    search_fields = ('ticker', )

@admin.register(StockPricesDays)
class StockPricesDaysAdmin(admin.ModelAdmin):
    list_display = ['company', 'idx', 'open', 'high', 'low', 'close', 'volume']
    list_filter = ('company', 'idx', )
