from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (PersonDim, GeneDim, Fact, FactNormalized)


@admin.register(PersonDim)
class PersonDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'person_code', 'gender', 'age_at_cdna', 'set_num')
    list_filter = ['person_code', 'set_num']


@admin.register(GeneDim)
class GeneDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'gene_code')


@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ('id', 'gene_dim', 'person_dim', 'amount')

@admin.register(FactNormalized)
class FactNormalizedAdmin(admin.ModelAdmin):
    list_display = ('id', 'gene_dim', 'person_dim', 'amount')

