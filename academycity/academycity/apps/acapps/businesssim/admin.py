from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (BusinesssimWeb, Participants, Institutions, GeneralLedgers, GeneralLedgerDetail, TrialBalance)


@admin.register(BusinesssimWeb)
class BusinesssimWebAdmin(admin.ModelAdmin):
    list_display = ('id', 'program_name', 'start_date', 'end_date', 'number_of_periods', 'number_of_participant')


@admin.register(Participants)
class ParticipantsAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'address', 'team')


@admin.register(Institutions)
class InstitutionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

