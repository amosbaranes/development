from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (PotentialWeb, TimeDim, CountryDim, MeasureGroupDim, MeasureDim, Fact, MinMaxCut)


@admin.register(PotentialWeb)
class PotentialWebAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_name')


@admin.register(TimeDim)
class TimeDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'year')


@admin.register(CountryDim)
class CountryDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'country_name', 'country_code')


@admin.register(MeasureGroupDim)
class MeasureGroupDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_name')


@admin.register(MeasureDim)
class MeasureDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'measure_group_dim', 'measure_name', 'measure_code')


@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_dim', 'country_dim', 'measure_dim', 'amount')
    list_filter = ['country_dim', 'measure_dim', 'time_dim']


@admin.register(MinMaxCut)
class MinMaxCutAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_dim', 'measure_dim', 'min', 'max')
