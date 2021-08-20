from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (Project, RBOIC, CountryRegion, CountryRating, Industry,
                     Country, GlobalIndustryAverages, CompanyInfo, CompanyData, ToDoList,
                     XBRLMainIndustryInfo, XBRLIndustryInfo, XBRLCompanyInfoInProcess, XBRLValuationAccounts,
                     XBRLCompanyInfo, XBRLValuationAccountsMatch)

# -*- coding: utf-8 -*-

from cms.admin.placeholderadmin import PlaceholderAdminMixin
from parler.admin import TranslatableAdmin, TranslatableStackedInline, TranslatableTabularInline


@admin.register(ToDoList)
class ToDoListAdmin(admin.ModelAdmin):
    list_display = ('priority', 'subject', 'id', 'user')
    list_filter = ('priority', )


@admin.register(Project)
class ProjectAdmin(TranslatableAdmin, PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'language_column', 'name', 'status', 'course_schedule', 'mature_marker_risk_premium',
                    'volatility_ratio', 'rf')
    fieldsets = (
        (None, {
            'fields': (
                'image',
                'course_schedule',
                'status',
                'mature_marker_risk_premium',
                'volatility_ratio',
                'rf',
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


@admin.register(RBOIC)
class RBOICAdmin(admin.ModelAdmin):
    list_display = ('from_ic', 'to_ic', 'rating', 'spread')


@admin.register(CountryRegion)
class CountryRegionAdmin(admin.ModelAdmin):
    list_display = ('pkey_region', 'region')


@admin.register(CountryRating)
class CountryRatingAdmin(admin.ModelAdmin):
    list_display = ('pkey_country_rating', 'country_rating', 'default_spread')


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('country', 'adj_default_spread', 'country_risk_premium', 'total_risk_premium')


@admin.register(GlobalIndustryAverages)
class GlobalIndustryAveragesAdmin(admin.ModelAdmin):
    list_display = ('industry_name', )


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('sic_code', 'sic_description', )


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'ticker', 'cik', 'industry', )
    list_filter = ('industry', )


@admin.register(CompanyData)
class CompanyDataAdmin(admin.ModelAdmin):
    list_display = ('company', 'year', )
    list_filter = ('year', )


@admin.register(XBRLMainIndustryInfo)
class XBRLMainIndustryInfoAdmin(admin.ModelAdmin):
    list_display = ('sic_code', 'sic_description')


@admin.register(XBRLIndustryInfo)
class XBRLIndustryInfoAdmin(admin.ModelAdmin):
    list_display = ('sic_code', 'main_sic', 'sic_description')
    list_filter = ('main_sic',)


@admin.register(XBRLCompanyInfoInProcess)
class XBRLCompanyInfoInProcessAdmin(admin.ModelAdmin):
    list_display = ('id', 'exchange', 'ticker', 'company_name', 'company_letter')
    list_filter = ('exchange', 'company_letter')


@admin.register(XBRLValuationAccounts)
class XBRLValuationAccountsAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'account', 'type')
    list_filter = ('type',)


@admin.register(XBRLValuationAccountsMatch)
class XBRLValuationAccountsMatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'year', 'account', 'match_account', 'accounting_standard')
    list_filter = ('company', 'year')


@admin.register(XBRLCompanyInfo)
class XBRLCompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'exchange', 'ticker', 'cik', 'company_name', 'company_letter')
    list_filter = ('exchange', 'company_letter')

