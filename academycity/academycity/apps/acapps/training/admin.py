from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (TrainingWeb, Instructors, Brigades, Battalions, Companys, Platoons, Squads, TestsStructures,
                     Compliances, Courses, Soldiers, Tests, TimeDim, SoldierFact,
                     DoubleShoot)


@admin.register(TrainingWeb)
class TrainingWebAdmin(admin.ModelAdmin):
    list_display = ('id', 'program_name', 'start_date', 'end_date')

@admin.register(Instructors)
class InstructorsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')

@admin.register(Brigades)
class BrigadesAdmin(admin.ModelAdmin):
    list_display = ('id', 'brigade_name')

@admin.register(Battalions)
class BattalionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'battalion_name', 'battalion_number')

@admin.register(Companys)
class CompanysAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name')

@admin.register(Platoons)
class PlatoonsAdmin(admin.ModelAdmin):
    list_display = ('id', 'platoon_name', 'platoon_number')

@admin.register(Squads)
class SquadsAdmin(admin.ModelAdmin):
    list_display = ('id', 'squad_name')

@admin.register(TestsStructures)
class TestsStructuresAdmin(admin.ModelAdmin):
    list_display = ('battalion', )

@admin.register(Compliances)
class CompliancesAdmin(admin.ModelAdmin):
    list_display = ('id', 'week', 'platoon')

@admin.register(Soldiers)
class SoldiersAdmin(admin.ModelAdmin):
    list_display = ('userid', 'first_name', 'last_name')

@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'start_date', 'end_date')

@admin.register(Tests)
class TestsAdmin(admin.ModelAdmin):
    list_display = ('soldier', 'test', 'grade')

@admin.register(TimeDim)
class TimeDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'month', 'day')

@admin.register(SoldierFact)
class SoldierFactAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'time_dim', 'soldier', 'test', 'value')

@admin.register(DoubleShoot)
class DoubleShootAdmin(admin.ModelAdmin):
    list_display = ('id', 'soldier')
