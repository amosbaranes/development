from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (TimeDim, CountryDim, CityDim, MeasureGroupDim, MeasureDim, CitiesFact,
                     MinMaxCut)


@admin.register(TimeDim)
class TimeDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'year')


@admin.register(CountryDim)
class CountryDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'country_name', 'country_code', )
    list_filter = ['country_name', 'country_code', 'country_cc']


@admin.register(MeasureGroupDim)
class MeasureGroupDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_name')


@admin.register(MeasureDim)
class MeasureDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'measure_group_dim', 'measure_name', 'description')


@admin.register(CitiesFact)
class WorldBankFactAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_dim', 'city_dim', 'measure_dim', 'amount')
    list_filter = ['measure_dim', 'time_dim', 'city_dim']

@admin.register(CityDim)
class CityDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'city_name')

@admin.register(MinMaxCut)
class MinMaxCutAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_dim', 'measure_dim', 'min', 'max')