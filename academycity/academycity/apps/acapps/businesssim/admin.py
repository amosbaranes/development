from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (BusinesssimWeb, Instructors, Participants, Institutions, GeneralLedgers, GeneralLedgerDetails,
                     TrialBalances, Friends)


@admin.register(BusinesssimWeb)
class BusinesssimWebAdmin(admin.ModelAdmin):
    list_display = ('id', 'program_name', 'start_date', 'end_date', 'number_of_periods', 'number_of_participants')


@admin.register(Participants)
class ParticipantsAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'address', 'team')


@admin.register(Institutions)
class InstitutionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact_person')


@admin.register(Instructors)
class InstructorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')


@admin.register(Friends)
class FriendsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

