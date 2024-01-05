from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (PersonDim, PersonGroupDim, GeneDim, GeneGroupDim, Fact, FactNormalized)


@admin.register(PersonDim)
class PersonDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'person_group_dim', 'person_code', 'gender', 'age_at_cdna', 'set_num')
    list_filter = ['person_code', 'set_num']


@admin.register(PersonGroupDim)
class PersonGroupDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_name')


@admin.register(GeneDim)
class GeneDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'gene_group_dim', 'gene_code')


@admin.register(GeneGroupDim)
class GeneGroupDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_name')


@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ('id', 'gene_dim', 'person_dim', 'amount')
    list_filter = ['gene_dim', 'person_dim']


@admin.register(FactNormalized)
class FactNormalizedAdmin(admin.ModelAdmin):
    list_display = ('id', 'gene_dim', 'person_dim', 'amount')
    list_filter = ['gene_dim', 'person_dim']

