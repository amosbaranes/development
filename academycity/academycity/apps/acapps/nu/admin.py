from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (FoodGroupDim, FoodDim)


@admin.register(FoodGroupDim)
class FoodGroupDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_name')


@admin.register(FoodDim)
class FoodDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'food_name')
    list_filter = ['food_name']

