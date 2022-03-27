from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import (Debug, DataAdvancedTabs, DataAdvancedTabsManager)


@admin.register(Debug)
class DebugAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']


@admin.register(DataAdvancedTabs)
class DataAdvancedTabsAdmin(admin.ModelAdmin):
    list_display = ['id', 'tab_name']


@admin.register(DataAdvancedTabsManager)
class DataAdvancedTabsManagerAdmin(admin.ModelAdmin):
    list_display = ['id', 'at_name']
