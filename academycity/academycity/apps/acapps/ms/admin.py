from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (Debug, PersonDim, PersonGroupDim, GeneDim, GeneGroupDim, Fact, FactNormalized, FactNormalizedTemp,
                     Temp, TempVar,
                     PCA, PCAData)


@admin.register(Debug)
class DebugAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']


@admin.register(PersonDim)
class PersonDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'person_group_dim', 'person_code', 'gender', 'age_at_cdna', 'set_num')
    list_filter = ['person_group_dim', 'person_code', 'set_num']


@admin.register(PersonGroupDim)
class PersonGroupDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_name')


@admin.register(GeneDim)
class GeneDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'gene_group_dim', 'gene_code', 'score')
    list_filter = ['gene_group_dim']


@admin.register(GeneGroupDim)
class GeneGroupDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_name')


@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ('id', 'gene_dim', 'person_dim', 'amount')
    list_filter = ['gene_dim', 'person_dim']


@admin.register(FactNormalized)
class FactNormalizedAdmin(admin.ModelAdmin):
    list_display = ('id', 'run_number', 'gene_dim', 'person_dim', 'amount')
    list_filter = ['run_number', 'gene_dim', 'person_dim']

@admin.register(FactNormalizedTemp)
class FactNormalizedTempAdmin(admin.ModelAdmin):
    list_display = ('id', 'run_number', 'gene_dim', 'person_dim', 'amount')
    list_filter = ['run_number', 'gene_dim', 'person_dim']

# Temp
@admin.register(Temp)
class TempAdmin(admin.ModelAdmin):
    list_display = ('id', 'idx')
    list_filter = ['idx']


@admin.register(TempVar)
class TempVarAdmin(admin.ModelAdmin):
    list_display = ('id', 'temp', 'gene_dim', 'amount', 'sign')
    list_filter = ['temp', 'gene_dim']

# PCA
@admin.register(PCA)
class PCAAdmin(admin.ModelAdmin):
    list_display = ('id', 'run_number', 'set', 'sub_set', 'component')
    list_filter = ['set', 'sub_set']

@admin.register(PCAData)
class PCADataAdmin(admin.ModelAdmin):
    list_display = ('id', 'pca', 'idx', 'amount')
    list_filter = ['pca']
