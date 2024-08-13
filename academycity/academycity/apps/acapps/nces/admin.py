from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (Debug ,TimeDim, CountryDim, RegionDim, DistrictDim, MeasureDim, Fact)


@admin.register(Debug)
class DebugAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']


@admin.register(TimeDim)
class TimeDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'year')


@admin.register(CountryDim)
class CountryDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'country_name', )
    list_filter = ['country_name']


@admin.register(RegionDim)
class RangeDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'region_name')
    list_filter = ['country_dim']


@admin.register(DistrictDim)
class DistrictDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'district_name')
    list_filter = ['region_dim']


@admin.register(MeasureDim)
class MeasureDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'measure_name')


@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_dim', 'district_dim', 'measure_dim', 'amount')
    list_filter = ['measure_dim', 'time_dim', 'district_dim']

