from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (TradesWeb)


@admin.register(TradesWeb)
class AccountingWebAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name')

