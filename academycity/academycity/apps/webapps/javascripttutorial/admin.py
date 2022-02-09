from django.contrib import admin
from .models import DataTabs


@admin.register(DataTabs)
class DataTabsAdmin(admin.ModelAdmin):
    list_display = ('id', 'tab_name', )


# Register your models here.
