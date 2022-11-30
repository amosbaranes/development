from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (TrainingWeb, Brigades, Battalions, Companys, Sections, Squads, Soldiers, PrivateSpecialty)


@admin.register(TrainingWeb)
class TrainingWebAdmin(admin.ModelAdmin):
    list_display = ('id', 'program_name', 'start_date', 'end_date')


@admin.register(Brigades)
class BrigadesAdmin(admin.ModelAdmin):
    list_display = ('id', 'brigade_name')


@admin.register(Battalions)
class BattalionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'battalion_name')


@admin.register(Companys)
class CompanysAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name')


@admin.register(Sections)
class SectionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'section_name')


@admin.register(Squads)
class SquadsAdmin(admin.ModelAdmin):
    list_display = ('id', 'squad_name')


@admin.register(Soldiers)
class SoldiersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'first_name', 'last_name')


@admin.register(PrivateSpecialty)
class PrivateSpecialtyAdmin(admin.ModelAdmin):
    list_display = ('id', 'soldier', 'specialty', 'test', 'value')
