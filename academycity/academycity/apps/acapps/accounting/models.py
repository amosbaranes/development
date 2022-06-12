from __future__ import unicode_literals
from django.db import models
from academycity.apps.core.sql import TruncateTableMixin


class AccountingWeb(TruncateTableMixin, models.Model):
    company_name = models.CharField(max_length=100, default='', blank=True, null=True)
    address = models.CharField(max_length=50, default='', blank=True, null=True)

    def __str__(self):
        return self.company_name


class Students(TruncateTableMixin, models.Model):
    accounting_web = models.ForeignKey(AccountingWeb, on_delete=models.CASCADE, default=1,
                                       related_name='accounting_students')
    first_name = models.CharField(max_length=50, default='', blank=True, null=True)
    last_name = models.CharField(max_length=50, default='', blank=True, null=True)
    email = models.CharField(max_length=50, default='', blank=True, null=True)
    phone = models.CharField(max_length=50, default='', blank=True, null=True)
    address = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return self.first_name+" "+self.last_name


class Payments(TruncateTableMixin, models.Model):
    accounting_web = models.ForeignKey(AccountingWeb, on_delete=models.CASCADE, default=1,
                                       related_name='accounting_payments')
    student = models.ForeignKey(Students, on_delete=models.CASCADE, default=1,
                                related_name='student_payments')
    created = models.DateField(auto_now_add=True)
    amount = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return str(self.student) + " - " + str(self.amount)


class Charges(TruncateTableMixin, models.Model):
    accounting_web = models.ForeignKey(AccountingWeb, on_delete=models.CASCADE, default=1,
                                       related_name='accounting_charges')
    student = models.ForeignKey(Students, on_delete=models.CASCADE, default=1,
                                related_name='student_charges')
    created = models.DateField(auto_now_add=True)
    amount = models.IntegerField(default=0, blank=True)
    reason = models.CharField(max_length=50, default='', blank=True, null=True)

    def __str__(self):
        return str(self.student) + " - " + str(self.amount)
