from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (Debug, VarDim, VarGroupDim, EntityDim, Fact, TempVar, Temp, FactNormalizedMinMax)


@admin.register(Debug)
class DebugAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']


@admin.register(VarGroupDim)
class VarGroupDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_name')
    list_filter = ['group_name']


@admin.register(VarDim)
class VarDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'var_code', 'var_group_dim', 'score', 'count0', 'count10', 'count15', 'count20')
    list_filter = ['var_code', 'var_group_dim']


@admin.register(EntityDim)
class EntityDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'entity_code')
    list_filter = ['entity_code']


@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ('id', 'var_dim', 'entity_dim', 'amount')
    list_filter = ['var_dim', 'entity_dim']


@admin.register(Temp)
class TempAdmin(admin.ModelAdmin):
    list_display = ('dep_var_dim', 'idx', )
    list_filter = ['dep_var_dim', 'idx']


@admin.register(TempVar)
class TempVarAdmin(admin.ModelAdmin):
    list_display = ('temp', 'var_dim', 'sign', 'amount')
    list_filter = ['temp', ]


@admin.register(FactNormalizedMinMax)
class FactNormalizedMinMaxAdmin(admin.ModelAdmin):
    list_display = ('id', 'dep_var_dim', 'var_dim', 'entity_dim', 'amount')
    list_filter = ['dep_var_dim', 'var_dim', 'entity_dim']

