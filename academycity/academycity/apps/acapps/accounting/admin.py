from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (Students, Payments, Charges, Expenses, AccountingWeb,
                     Locations, GeneralLedgers, GeneralLedgerDetail, TimeDim, TrialBalance)


@admin.register(AccountingWeb)
class AccountingWebAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name')


@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'address', 'accounting_web')


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'amount')


@admin.register(Charges)
class ChargesAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'reason', 'amount')


@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'amount', 'comment')


@admin.register(Locations)
class LocationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'name')


@admin.register(GeneralLedgers)
class GeneralLedgersAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_dim', 'location', 'comment')


@admin.register(GeneralLedgerDetail)
class GeneralLedgerDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'generalledger', 'account', 'amount', 'comment')


@admin.register(TimeDim)
class TimeDimAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'quarter', 'month', 'day')


@admin.register(TrialBalance)
class TrialBalanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', "level", 'time_dim', 'account', 'amount')

