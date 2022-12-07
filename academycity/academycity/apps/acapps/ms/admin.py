from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (PersonDim, GeneDim, Fact)


@admin.register(PersonDim)
class PersonDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'person_code')


@admin.register(GeneDim)
class GeneDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'gene_code')


@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ('id', 'gene_dim', 'person_dim', 'amount')

