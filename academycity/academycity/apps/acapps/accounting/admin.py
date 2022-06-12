from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (Students, Payments, Charges, AccountingWeb)


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

