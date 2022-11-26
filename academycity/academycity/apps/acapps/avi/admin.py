from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (TimeDim, CountryDim, MeasureGroupDim, MeasureDim, WorldBankFact)


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
    list_display = ('id', 'measure_name', 'measure_code')


@admin.register(WorldBankFact)
class WorldBankFactAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_dim', 'country_dim', 'measure_dim', 'amount')

