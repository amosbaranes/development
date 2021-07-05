from django.contrib import admin
from .models import (Institution, Profile)


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'institution', 'created', 'image']
    list_filter = ['institution', 'created', 'user']


