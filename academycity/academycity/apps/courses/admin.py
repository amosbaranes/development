# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from cms.admin.placeholderadmin import PlaceholderAdminMixin
from parler.admin import TranslatableAdmin, TranslatableStackedInline, TranslatableTabularInline

from .models import (Department, Course, Syllabus, Section, SubSection, CourseSchedule, CourseScheduleUser,
                     Order, OrderItem,
                     ChartOfAccounts, Coupon,
                     Assignment, AssignmentUser,
                     Team)


class DepartmentAdmin(TranslatableAdmin, PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('language_column', 'name', 'active',)
    fieldsets = (
        (None, {
         'fields': (
            'image',
            'active',
            'order',
         )
        }),
        (_('Translated Fields'), {
            'fields': (
                'name',
                'slug',
            ),
        }),
    )

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


# ----
class SectionStacked(TranslatableStackedInline):
    model = Section
    extra = 1


class SectionTabular(TranslatableTabularInline):
    model = Section
    extra = 1


# ---
class CourseAdmin(TranslatableAdmin, PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('language_column', 'name', 'department', 'active',)
    fieldsets = (
        (None, {
            'fields': (
                'image',
                'department',
                'active',
                'order',
                'instructors',
                'is_team',
                'link_app',
                'link_model',
            )
        }),
        (_('Translated Fields'), {
            'fields': (
                'name',
                'slug',
            ),
        }),
    )

    inlines = [SectionTabular]

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


class SyllabusAdmin(TranslatableAdmin, PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('language_column', 'name', 'course', )
    fieldsets = (
        (None, {
            'fields': (
                'image',
                'course',
            )
        }),
        (_('Translated Fields'), {
            'fields': (
                'name',
                'slug',
            ),
        }),
    )

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


class SectionAdmin(TranslatableAdmin, PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('language_column', 'name','course', )
    fieldsets = (
        (None, {
            'fields': (
                'course',
                'order',
            )
        }),
        (_('Translated Fields'), {
            'fields': (
                'name',
                'slug',
            ),
        }),
    )

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


class SubSectionAdmin(TranslatableAdmin, PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('language_column', 'name', 'section', )
    fieldsets = (
        (None, {
            'fields': (
                'section',
                'order',
            )
        }),
        (_('Translated Fields'), {
            'fields': (
                'name',
                'slug',
            ),
        }),
    )

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


class CourseScheduleAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'active', )

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


class CourseScheduleUserAdmin(admin.ModelAdmin):
    list_display = ('course_schedule', 'user', 'created_date', 'active', 'graduated', 'paid', 'slug', 'team')
    list_filter = ['course_schedule', 'user']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]


class ChartOfAccountsAdmin(TranslatableAdmin, PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('language_column', 'account', 'parent', 'account_type', 'id', )
    fieldsets = (
        (None, {
         'fields': (
             'code',
             'parent',
             'account_type',
         )
        }),
        (_('Translated Fields'), {
            'fields': (
                'account',
            ),
        }),
    )


class CouponAdmin(admin.ModelAdmin):
    list_display = ['product', 'code', 'valid_from', 'valid_to', 'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']


class AssignmentUserAdmin(admin.ModelAdmin):
    pass


class AssignmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'course_schedule', 'name', 'image']


admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(AssignmentUser, AssignmentUserAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Syllabus, SyllabusAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(SubSection, SubSectionAdmin)

admin.site.register(CourseSchedule, CourseScheduleAdmin)
admin.site.register(CourseScheduleUser, CourseScheduleUserAdmin)

admin.site.register(ChartOfAccounts, ChartOfAccountsAdmin)

# class ModuleInline(admin.StackedInline):    model = Module
# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
# list_display = ['title', 'subject', 'created']
# list_filter = ['created', 'subject']
# search_fields = ['title', 'overview']
# prepopulated_fields = {'slug': ('title',)}
# inlines = [ModuleInline]
