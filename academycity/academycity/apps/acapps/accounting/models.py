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
    user_id = models.CharField(max_length=100, default='', blank=True, null=True)
    twitter = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return self.first_name+" "+self.last_name


class Payments(TruncateTableMixin, models.Model):
    accounting_web = models.ForeignKey(AccountingWeb, on_delete=models.CASCADE, default=1,
                                       related_name='accounting_payments')
    student = models.ForeignKey(Students, on_delete=models.CASCADE, default=1,
                                related_name='student_payments')
    created = models.DateField(auto_now_add=True)
    amount = models.IntegerField(default=0, blank=True)
    reason = models.CharField(max_length=50, default='', blank=True, null=True)

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


class Expenses(TruncateTableMixin, models.Model):
    accounting_web = models.ForeignKey(AccountingWeb, on_delete=models.CASCADE, default=1,
                                       related_name='accounting_expenses')

    created = models.DateField(auto_now_add=True)
    amount = models.IntegerField(default=0, blank=True)
    account = models.IntegerField(default=0, blank=True, null=True)
    comment = models.CharField(max_length=256, default='', blank=True, null=True)

    def __str__(self):
        return str(self.account) + " - " + str(self.amount) + " - " + str(self.comment)


class Locations(TruncateTableMixin, models.Model):
    accounting_web = models.ForeignKey(AccountingWeb, on_delete=models.CASCADE, default=1,
                                       related_name='accounting_location')
    created = models.DateField(auto_now_add=True)
    location = models.CharField(max_length=256, default='', blank=True, null=True)
    name = models.CharField(max_length=256, default='', blank=True, null=True)
    address = models.CharField(max_length=256, default='', blank=True, null=True)
    city = models.CharField(max_length=100, default='', blank=True, null=True)
    state = models.CharField(max_length=10, default='', blank=True, null=True)
    zip = models.CharField(max_length=15, default='', blank=True, null=True)

    def __str__(self):
        return str(self.location)  # + " - " + str(self.address) + " - " + str(self.city) + " - " + str(self.state)


class TimeDim(TruncateTableMixin, models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    year = models.PositiveSmallIntegerField(default=0)
    quarter = models.PositiveSmallIntegerField(default=0)
    month = models.PositiveSmallIntegerField(default=0)
    day = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.id)


class GeneralLedgers(TruncateTableMixin, models.Model):
    accounting_web = models.ForeignKey(AccountingWeb, on_delete=models.CASCADE, default=1,
                                       related_name='accounting_general_ledger')
    location = models.ForeignKey(Locations, on_delete=models.CASCADE, default=1,
                                 related_name='location_general_ledger')
    time_dim = models.ForeignKey(TimeDim, on_delete=models.CASCADE, default=1,
                                 related_name='general_ledger_timedim')
    comment = models.CharField(max_length=256, default='', blank=True, null=True)

    def __str__(self):
        return str(self.id) + " - " + str(self.location) + " - " + str(self.comment)


class GeneralLedgerDetail(TruncateTableMixin, models.Model):

    class Meta:
        verbose_name = 'GeneralLedgerDetail'
        verbose_name_plural = 'GeneralLedgerDetail'
        ordering = ['generalledger', 'account']

    accounting_web = models.ForeignKey(AccountingWeb, on_delete=models.CASCADE, default=1,
                                       related_name='accounting_general_ledger_detail')
    generalledger = models.ForeignKey(GeneralLedgers, on_delete=models.CASCADE, default=1,
                                      related_name='gl_general_ledger_detail')
    account = models.IntegerField(default=0, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    comment = models.CharField(max_length=256, default='', blank=True, null=True)

    def __str__(self):
        return str(self.account) + " - " + str(self.amount) + " - " + str(self.comment)


class TrialBalance(TruncateTableMixin, models.Model):
    accounting_web = models.ForeignKey(AccountingWeb, on_delete=models.CASCADE, default=1,
                                       related_name='accounting_trial_balance')
    location = models.ForeignKey(Locations, on_delete=models.CASCADE, default=1,
                                 related_name='location_trial_balance')
    time_dim = models.ForeignKey(TimeDim, on_delete=models.CASCADE, default=1,
                                 related_name='trial_balance_timedim')

    level = models.SmallIntegerField(default=0, blank=True, null=True)
    account = models.IntegerField(default=0, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.location) + " - " + str(self.time_dim) + " - " + str(self.account) + ": " + str(self.amount)

