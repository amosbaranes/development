from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (EntityDim, MeasureGroupDim, RangeDim, MeasureDim,
                     OutputFact, Fact, RelImpFact, MinMaxCut)


@admin.register(EntityDim)
class EntityDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'entity_id', 'entity_serial', 'entity_race', )
    list_filter = ['entity_id', 'entity_serial', 'entity_race']


@admin.register(MeasureGroupDim)
class MeasureGroupDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_name')


@admin.register(RangeDim)
class RangeDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'range_name')


@admin.register(MeasureDim)
class MeasureDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'measure_group_dim', 'measure_name', 'measure_code', 'description')
    list_filter = ['measure_group_dim']


@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ('id', 'entity_dim', 'measure_dim', 'amount')
    list_filter = ['measure_dim', 'entity_dim']


@admin.register(OutputFact)
class OutputFactAdmin(admin.ModelAdmin):
    list_display = ('id', 'range_dim', 'entity_dim', 'measure_dim', 'amount')
    list_filter = ['range_dim', 'measure_dim', 'entity_dim']


@admin.register(RelImpFact)
class RelImpFactAdmin(admin.ModelAdmin):
    list_display = ('id', 'range_dim', 'measure_dim', 'measure_group_dim', 'amount')
    list_filter = ['range_dim', 'measure_dim', 'measure_group_dim']


@admin.register(MinMaxCut)
class MinMaxCutAdmin(admin.ModelAdmin):
    list_display = ('id', 'measure_dim', 'min', 'max')
    list_filter = ['measure_dim']
