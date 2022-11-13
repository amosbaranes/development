from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (TrainingWeb)


@admin.register(TrainingWeb)
class TrainingWebAdmin(admin.ModelAdmin):
    list_display = ('id', 'program_name', 'start_date', 'end_date', 'number_of_periods', 'number_of_participants')

