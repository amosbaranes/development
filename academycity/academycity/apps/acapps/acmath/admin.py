from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (AcMathWeb)


@admin.register(AcMathWeb)
class AcMathWebAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name')

