from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (SWOTClock, SWOTClockData)


class SWOTClockAdmin(admin.ModelAdmin):
    list_display = ['swot_user', 'file_name']
    list_filter = ['swot_user']
    search_fields = ['swot_user']


class SWOTClockDataAdmin(admin.ModelAdmin):
    list_display = ['swot_clock', 'field_id', 'field_value']
    list_filter = ['swot_clock']
    search_fields = ['swot_clock']


admin.site.register(SWOTClock, SWOTClockAdmin)
admin.site.register(SWOTClockData, SWOTClockDataAdmin)