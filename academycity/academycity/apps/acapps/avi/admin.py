from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (TimeDim, CountryDim, MeasureGroupDim, MeasureDim, UniversityDim, WorldBankFact, UniversityRankFact)


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
    list_display = ('id', 'measure_name', 'measure_code')


@admin.register(WorldBankFact)
class WorldBankFactAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_dim', 'country_dim', 'measure_dim', 'amount')
    list_filter = ['measure_dim', 'time_dim', 'country_dim']


@admin.register(UniversityRankFact)
class UniversityRankFactAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_dim', 'country_dim', 'university_dim', 'measure_dim', 'amount')
    list_filter = ['measure_dim', 'time_dim', 'country_dim']


@admin.register(UniversityDim)
class UniversityDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'university_name', 'country_dim')
    list_filter = ['university_name', 'country_dim']

