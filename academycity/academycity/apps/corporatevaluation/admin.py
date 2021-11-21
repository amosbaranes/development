from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (Project, RBOIC, CountryRegion, CountryRating, Industry,
                     Country, GlobalIndustryAverages, CompanyInfo, CompanyData, ToDoList,
                     XBRLMainIndustryInfo, XBRLIndustryInfo, XBRLCompanyInfoInProcess, XBRLValuationAccounts,
                     XBRLCompanyInfo, XBRLValuationAccountsMatch, XBRLValuationStatementsAccounts,
                     XBRLRegion, XBRLCountry, XBRLCountryYearData,XBRLRegionYearData,
                     XBRLHistoricalReturnsSP, XBRLSPMoodys,
                     XBRLSPEarningForecast, XBRLSPStatistics,
                     XBRLCountriesOfOperations, XBRLRegionsOfOperations, XBRLYearsCompanyOperations,
                     XBRLIndustryBetasOfOperations)

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
    list_display = ('id', 'exchange', 'ticker', 'sic', 'company_name', 'company_letter', 'is_error')
    list_filter = ('exchange', 'is_error', 'company_letter')
    search_fields = ('ticker', )


@admin.register(XBRLValuationAccounts)
class XBRLValuationAccountsAdmin(admin.ModelAdmin):
    list_display = ('id', 'sic', 'order', 'account', 'type', 'statement', 'scale')
    list_filter = ('type', 'statement')


@admin.register(XBRLValuationStatementsAccounts)
class XBRLValuationStatementsAccountsAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'statement')


@admin.register(XBRLValuationAccountsMatch)
class XBRLValuationAccountsMatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'year', 'account', 'match_account', 'accounting_standard')
    list_filter = ('company', 'year')


@admin.register(XBRLCompanyInfo)
class XBRLCompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'exchange', 'ticker', 'cik', 'company_name', 'company_letter')
    list_filter = ('exchange', 'company_letter')
    search_fields = ('ticker', )


@admin.register(XBRLRegion)
class XBRLRegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'full_name', 'updated_adamodar')
    list_filter = ('updated_adamodar', )


@admin.register(XBRLCountry)
class XBRLCountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region', 'updated_adamodar')
    list_filter = ('region', 'updated_adamodar')
    search_fields = ('name', )


@admin.register(XBRLCountryYearData)
class XBRLCountryYearDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'year'
                    , 'sp_rating'
                    , 'moodys_rate_completed_by_sp'
                    , 'country_risk_premium_rating'
                    , 'cds'
                    , 'excess_cds_spread_over_us_cds'
                    , 'rating_based_default_spread'
                    , 'composite_risk_rating'
                    , 'tax_rate'
                    , 'gdp'
                    # , 'moodys_rating'
                    )
    list_filter = ('country', 'year',)
    search_fields = ('country', )


@admin.register(XBRLRegionYearData)
class XBRLRegionYearDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'region', 'year'
                    , 'moodys_rate_completed_by_sp'
                    , 'country_risk_premium_rating'
                    , 'rating_based_default_spread'
                    , 'tax_rate'
                    )
    list_filter = ('region', 'year',)
    search_fields = ('region', )


@admin.register(XBRLHistoricalReturnsSP)
class XBRLHistoricalReturnsSPAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'tb3ms', 'stock_tbill_return', 'stock_tbonds_return', 'stock_baa_return',
                    'risk_premium',
                    'return_on_sp500_real', 'return_on_tbond_real', 'tb3ms_rate_real', 'return_on_bbb_real',
                    'return_on_sp500', 'tb3ms_rate', 'return_on_tbond', 'return_on_bbb', 'aaa_rate',
                    'return_on_aaa', 'bbb_rate', 'tb10y', 'dividends', 'sp500', 'dividend_yield',
                    'return_on_real_estate', 'home_prices', 'cpi')
    list_filter = ('year',)


@admin.register(XBRLSPMoodys)
class XBRLSPMoodysAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'sp', 'moodys', 'score_from', 'score_to', 'default_spread')
    list_filter = ('year',)


@admin.register(XBRLSPEarningForecast)
class XBRLSPEarningForecastAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'year', 'quarter', 'forecast', 'actual', 'today_price', 'yesterday_price',
                    'date', 'next_release_date')
    list_filter = ('company', 'year', 'quarter',)


@admin.register(XBRLSPStatistics)
class XBRLSPStatisticsAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'next_release_date', 'mean_abs_price_change', 'mean_abs_actual_forecast_change',
                    'correlation_afp', 'updated', 'straddle_price', 'butterfly_price', 'announcement_time')


@admin.register(XBRLCountriesOfOperations)
class XBRLCountriesOfOperationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_year', 'country')


@admin.register(XBRLRegionsOfOperations)
class XBRLRegionsOfOperationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_year', 'region')


@admin.register(XBRLYearsCompanyOperations)
class XBRLYearsCompanyOperationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'year')


@admin.register(XBRLIndustryBetasOfOperations)
class XBRLIndustryBetasOfOperationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_year', 'industry')
