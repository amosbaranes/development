from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (ChWeb, Branches, Departments, BranchDepartments, Cells, Members, Children)


@admin.register(ChWeb)
class ChWebAdmin(admin.ModelAdmin):
    list_display = ('id', 'program_name', 'start_date', 'end_date')


@admin.register(Branches)
class BranchesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'branch_leader', )


@admin.register(Departments)
class DepartmentsAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(BranchDepartments)
class BranchDepartmentsAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(Cells)
class CellsAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(Members)
class MembersAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'branch')


@admin.register(Children)
class ChildrenAdmin(admin.ModelAdmin):
    list_display = ('id', )

