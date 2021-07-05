from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import (Debug)


@admin.register(Debug)
class DebugAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']

