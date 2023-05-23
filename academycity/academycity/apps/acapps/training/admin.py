from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (TrainingWeb, Instructors, Brigades, Battalions, Companys, Platoons, Squads, TestsStructures,
                     ComplianceWeeks, ComplianceDays, Courses, Soldiers, Tests, TimeDim, SoldierFact,
                     SoldierQualificationFact,
                     TestEvents, TestsForEvents, SoldiersForEvents, GradesForEvents,
                     InventoryCategorys,Inventorys,TestsVariables, TestsForVariables, Periods, UnitSoldiers,
                     DoubleShoot, DoubleShootMembers,
                     ToDoList)


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

@admin.register(ComplianceWeeks)
class ComplianceWeeksAdmin(admin.ModelAdmin):
    list_display = ('id', 'battalion', 'unit')

@admin.register(ComplianceDays)
class ComplianceDaysAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_dim', 'compliance_week')

@admin.register(Soldiers)
class SoldiersAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'userid', 'first_name', 'last_name')

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

@admin.register(TestEvents)
class TestEventsAdmin(admin.ModelAdmin):
    list_display = ('id', 'period', 'instructor', 'time_dim', 'test_event_name')

@admin.register(TestsForEvents)
class TestsForEventsAdmin(admin.ModelAdmin):
    list_display = ('id', 'testevent', 'test_number', 'value')

@admin.register(SoldiersForEvents)
class SoldiersForEventsAdmin(admin.ModelAdmin):
    list_display = ('id', 'testevent', 'soldier_number', 'value')

@admin.register(GradesForEvents)
class SoldiersForEventsAdmin(admin.ModelAdmin):
    list_display = ('id', 'testevent', 'soldiersforevent', 'testsforevent', 'value')

#
@admin.register(Inventorys)
class InventorysAdmin(admin.ModelAdmin):
    list_display = ('id', 'inventorycategory', 'inventory_number')

@admin.register(InventoryCategorys)
class InventoryCategorysAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_number', 'pn', 'category_name', 'category_name_1', 'category_name_2')

@admin.register(TestsVariables)
class TestsVariablesAdmin(admin.ModelAdmin):
    list_display = ('id', 'variable_name')

@admin.register(TestsForVariables)
class TestsForVariablesAdmin(admin.ModelAdmin):
    list_display = ('id', 'testsvariable', 'test_number', 'value')
#

@admin.register(DoubleShoot)
class DoubleShootAdmin(admin.ModelAdmin):
    list_display = ('id', 'soldier')

@admin.register(DoubleShootMembers)
class DoubleShootMembersAdmin(admin.ModelAdmin):
    list_display = ('ds_id', 'ds_name')

@admin.register(Periods)
class DoubleShootAdmin(admin.ModelAdmin):
    list_display = ('id', 'battalion', 'period_number', 'period_name')

@admin.register(UnitSoldiers)
class UnitSoldiersAdmin(admin.ModelAdmin):
    list_display = ('id', 'period', 'soldier', 'unit_number')

@admin.register(SoldierQualificationFact)
class SoldierQualificationFactAdmin(admin.ModelAdmin):
    list_display = ('id', 'soldier', 'skill', 'value')

@admin.register(ToDoList)
class ToDoListAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'description', 'priority', "is_active")
