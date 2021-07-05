# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from parler.admin import TranslatableAdmin, TranslatableStackedInline, TranslatableTabularInline

# --
from .models import (GameType, Segment, Attribute, Game,
                     Period, SchedulePeriodDate,
                     RandD, RandD_Attribute,
                     Product, ProductTypeAttribute,
                     ProductPeriodData, ProductPeriodDataDetail,
                     HumanResourcesPeriodData, HumanResourcesPeriodDataDetail, HumanResourcesTypeAttribute,
                     ManufacturingPeriodData, ManufacturingPeriodDataDetail, ManufacturingTypeAttribute,
                     Distributor, DistributorAttribute, DistributorSegment,
                     GDistributor, GDistributorPeriodData, GDistributorPeriodDataDetail,
                     FinanceType, FinanceTypeAttribute, Finance, FinancePeriodData, FinancePeriodDataDetail)


class GameTypeAdmin(TranslatableAdmin, PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('language_column', 'id', 'name', )
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


class SegmentAdmin(TranslatableAdmin, PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('language_column', 'id', 'name', 'game_type')
    fieldsets = (
        (None, {
         'fields': (
             'image',
             'game_type',
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


class AttributeAdmin(TranslatableAdmin, PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('language_column', 'id', 'name', 'segment', 'start_optimal_value',)
    fieldsets = (
        (None, {
         'fields': (
             'image',
             'order',
             'segment',
             'start_optimal_value', 'tau_improvments', 'tau_miss_match',
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


class DistributorSegmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'distributor', 'segment', 'percentage')


class DistributorAdmin(TranslatableAdmin, PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('language_column', 'id', 'name', 'game_type', 'number_of_location', 'logistic_support')
    fieldsets = (
        (None, {
         'fields': (
             'image',
             'game_type',
             'number_of_location', 'logistic_support',
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


class DistributorAttributeAdmin(TranslatableAdmin, PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('language_column', 'id', 'order', 'name', 'distributor', 'min', 'max')
    fieldsets = (
        (None, {
         'fields': (
             'image',
             'distributor',
             'min', 'max',
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


# ==========================================================================
class GameAdmin(TranslatableAdmin, PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('language_column', 'id', 'name', 'game_type', 'course_schedule', 'status',
                    'number_of_periods', 'current_period_number', 'start_period', 'current_period',
                    'period_type')
    fieldsets = (
        (None, {
         'fields': (
            'image',
            'game_type',
            'course_schedule',
            'status',
            'number_of_periods',
            'current_period_number',
            'period_type',
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


class PeriodAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'period', 'period_number')


class SchedulePeriodDateAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'date_time', 'period_number')


class RandDAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'period', 'team', 'segment', 'scu_per_unit',
                    'prime_cost_per_unit', 'project_expenditure')


class RandDArrtibuteAdmin(admin.ModelAdmin):
    list_display = ('id', 'randd', 'attribute', 'value', 'index')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'team', 'randd', 'created_period', 'abundant_period')


class ProductPeriodDataAdmin(admin.ModelAdmin):
    list_display = ('id', )


class ProductPeriodDataDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_type_attribute')


class HumanResourcesPeriodDataAdmin(admin.ModelAdmin):
    list_display = ('id', )


class HumanResourcesPeriodDataDetailAdmin(admin.ModelAdmin):
    list_display = ('id', )


class ManufacturingPeriodDataAdmin(admin.ModelAdmin):
    list_display = ('id', )


class ManufacturingPeriodDataDetailAdmin(admin.ModelAdmin):
    list_display = ('id', )


class ProductTypeAttributeAdmin(TranslatableAdmin, PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('language_column', 'id', 'name', 'segment', 'min', 'amount', 'max')
    fieldsets = (
        (None, {
         'fields': (
            'image',
            'segment',
            'category',
            'account',
            'amount',
            'min',
            'max',
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


class ManufacturingTypeAttributeAdmin(TranslatableAdmin, PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('language_column', 'id', 'name', 'amount', 'min', 'max')
    fieldsets = (
        (None, {
         'fields': (
            'image',
            'category',
            'account',
            'amount',
            'min',
            'max',
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


class HumanResourcesTypeAttributeAdmin(TranslatableAdmin, PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('language_column', 'id', 'name', 'amount', 'min', 'max',)
    fieldsets = (
        (None, {
         'fields': (
            'image',
            'category',
            'account',
            'amount',
            'min',
            'max',
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


class GDistributorAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'distributor')


class GDistributorPeriodDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'g_distributor', 'period')


class GDistributorPeriodDataDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'g_distributor_data', 'distributor_attribute', 'amount')


class FinanceTypeAdmin(TranslatableAdmin, PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('language_column', 'id', 'name', 'game_type')
    fieldsets = (
        (None, {
         'fields': (
            'image',
            'game_type',
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


class FinanceTypeAttributeAdmin(TranslatableAdmin, PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('language_column', 'id', 'name', 'finance_type')
    fieldsets = (
        (None, {
         'fields': (
            'image',
            'finance_type',
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


class FinanceAdmin(admin.ModelAdmin):
    list_display = ('id', )


class FinancePeriodDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'finance')


class FinancePeriodDataDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount')


admin.site.register(FinanceType, FinanceTypeAdmin)
admin.site.register(FinanceTypeAttribute, FinanceTypeAttributeAdmin)
admin.site.register(Finance, FinanceAdmin)
admin.site.register(FinancePeriodData, FinanceAdmin)
admin.site.register(FinancePeriodDataDetail, FinanceAdmin)

admin.site.register(Distributor, DistributorAdmin)
admin.site.register(DistributorAttribute, DistributorAttributeAdmin)
admin.site.register(DistributorSegment, DistributorSegmentAdmin)
admin.site.register(GDistributor, GDistributorAdmin)
admin.site.register(GDistributorPeriodData, GDistributorPeriodDataAdmin)
admin.site.register(GDistributorPeriodDataDetail, GDistributorPeriodDataDetailAdmin)

admin.site.register(GameType, GameTypeAdmin)
admin.site.register(Segment, SegmentAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Game, GameAdmin)

admin.site.register(Period, PeriodAdmin)
admin.site.register(SchedulePeriodDate, SchedulePeriodDateAdmin)
admin.site.register(RandD, RandDAdmin)
admin.site.register(RandD_Attribute, RandDArrtibuteAdmin)

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductPeriodData, ProductPeriodDataAdmin)
admin.site.register(ProductPeriodDataDetail, ProductPeriodDataDetailAdmin)
admin.site.register(ProductTypeAttribute, ProductTypeAttributeAdmin)

admin.site.register(ManufacturingPeriodData, ManufacturingPeriodDataAdmin)
admin.site.register(ManufacturingPeriodDataDetail, ManufacturingPeriodDataDetailAdmin)
admin.site.register(ManufacturingTypeAttribute, ManufacturingTypeAttributeAdmin)

admin.site.register(HumanResourcesPeriodData, HumanResourcesPeriodDataAdmin)
admin.site.register(HumanResourcesPeriodDataDetail, HumanResourcesPeriodDataDetailAdmin)
admin.site.register(HumanResourcesTypeAttribute, HumanResourcesTypeAttributeAdmin)

