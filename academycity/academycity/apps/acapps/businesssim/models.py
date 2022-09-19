from __future__ import unicode_literals
from django.db import models
from academycity.apps.core.sql import TruncateTableMixin


class BusinesssimWeb(TruncateTableMixin, models.Model):
    program_name = models.CharField(max_length=100, default='', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    number_of_periods = models.SmallIntegerField(default=9)
    number_of_participant = models.SmallIntegerField(default=9)

    def __str__(self):
        return self.program_name


class Institutions(TruncateTableMixin, models.Model):
    name = models.CharField(max_length=50, default='', blank=True, null=True)
    contact_person = models.CharField(max_length=50, default='', blank=True, null=True)
    email = models.CharField(max_length=50, default='', blank=True, null=True)
    phone = models.CharField(max_length=50, default='', blank=True, null=True)
    address = models.CharField(max_length=100, default='', blank=True, null=True)
    country = models.CharField(max_length=100, default='', blank=True, null=True)
    State = models.CharField(max_length=20, default='', blank=True, null=True)
    city = models.CharField(max_length=50, default='', blank=True, null=True)
    zip = models.CharField(max_length=15, default='', blank=True, null=True)


class Instructors(TruncateTableMixin, models.Model):
    businesssimm_web = models.ManyToManyField(BusinesssimWeb, related_name='businesssimm_instructors')
    institution = models.ManyToManyField(Institutions, related_name='institution_instructors')
    first_name = models.CharField(max_length=50, default='', blank=True, null=True)
    last_name = models.CharField(max_length=50, default='', blank=True, null=True)
    email = models.CharField(max_length=50, default='', blank=True, null=True)
    phone = models.CharField(max_length=50, default='', blank=True, null=True)
    address = models.CharField(max_length=100, default='', blank=True, null=True)
    country = models.CharField(max_length=100, default='', blank=True, null=True)
    State = models.CharField(max_length=20, default='', blank=True, null=True)
    city = models.CharField(max_length=50, default='', blank=True, null=True)
    zip = models.CharField(max_length=15, default='', blank=True, null=True)
    user_id = models.CharField(max_length=10, default='', blank=True, null=True)

    def __str__(self):
        return self.first_name+" "+self.last_name


class Teams(TruncateTableMixin, models.Model):
    businesssimm_web = models.ForeignKey(BusinesssimWeb, on_delete=models.CASCADE, default=1,
                                         related_name='businesssimm_teams')
    team_name = models.CharField(max_length=50, default='', blank=True, null=True)
    team_manager = models.CharField(max_length=50, default='', blank=True, null=True)


class Participants(TruncateTableMixin, models.Model):
    businesssimm_web = models.ForeignKey(BusinesssimWeb, on_delete=models.CASCADE, default=1,
                                         related_name='businesssimm_participants')
    institution = models.ForeignKey(Institutions, on_delete=models.CASCADE, default=1,
                                    related_name='institution_participants')
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, default=1,
                             related_name='team_participants')
    first_name = models.CharField(max_length=50, default='', blank=True, null=True)
    last_name = models.CharField(max_length=50, default='', blank=True, null=True)
    email = models.CharField(max_length=50, default='', blank=True, null=True)
    phone = models.CharField(max_length=50, default='', blank=True, null=True)
    address = models.CharField(max_length=100, default='', blank=True, null=True)
    country = models.CharField(max_length=100, default='', blank=True, null=True)
    State = models.CharField(max_length=20, default='', blank=True, null=True)
    city = models.CharField(max_length=50, default='', blank=True, null=True)
    zip = models.CharField(max_length=15, default='', blank=True, null=True)
    user_id = models.CharField(max_length=10, default='', blank=True, null=True)
    position = models.CharField(max_length=20, default='', blank=True, null=True)

    def __str__(self):
        return self.first_name+" "+self.last_name


# R&D
class RandDs(TruncateTableMixin, models.Model):
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, default=1,
                             related_name='team_randds')
    created_period = models.SmallIntegerField(default=1)
    project_name = models.CharField(max_length=50, default='new')
    prime_cost = models.IntegerField(default=100)
    investment = models.IntegerField(default=1000000)


class RandDProperties(TruncateTableMixin, models.Model):
    randd = models.ForeignKey(RandDs, on_delete=models.CASCADE, default=1,
                              related_name='randd_properties')
    property = models.CharField(max_length=50, default='new', blank=True, null=True)
    value = models.SmallIntegerField(default=20)


# Products
class Products(TruncateTableMixin, models.Model):
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, default=1, related_name='team_products')
    randd = models.ForeignKey(RandDs, on_delete=models.CASCADE, default=1, related_name='randd_products')
    name = models.CharField(max_length=50, default='new product')
    created_period = models.SmallIntegerField(default=1)
    abandon_period = models.SmallIntegerField(default=-1)


class ProductPeriods(TruncateTableMixin, models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, default=1, related_name='product_periods')
    period = models.SmallIntegerField(default=1)
    retail_price = models.SmallIntegerField(400)
    planned_production = models.IntegerField(default=10000)
    planned_safety_stock = models.IntegerField(default=1000)


# Marketing
class Marketing(TruncateTableMixin, models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, default=1, related_name='product_marketing')
    period = models.SmallIntegerField(default=1)
    channel = models.CharField(max_length=25, default='')
    amount = models.IntegerField(default=500000)


class Branding(TruncateTableMixin, models.Model):
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, default=1, related_name='team_branding')
    period = models.SmallIntegerField(default=1)


class Distribution(TruncateTableMixin, models.Model):
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, default=1, related_name='team_distribution')
    period = models.SmallIntegerField(default=1)
    type = models.CharField(max_length=25, default='')
    extra_support = models.IntegerField(500000)
    retail_margin = models.SmallIntegerField(35)


# Manufacturing
class Manufacturing(TruncateTableMixin, models.Model):
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, default=1, related_name='team_manufacturing')
    period = models.SmallIntegerField(default=1)
    add_employees = models.SmallIntegerField(default=1)
    add_plant_size = models.SmallIntegerField(default=1)
    efficiency_improvement = models.IntegerField(default=10000)
    supplier_relation = models.IntegerField(default=10000)
    raw_material_inventory = models.SmallIntegerField(default=1)
    average_salary = models.IntegerField(default=20000)
    training = models.SmallIntegerField(default=40)
    quality_system = models.IntegerField(default=150000)
    inspection = models.SmallIntegerField(default=15)


# Finance
class Finance(TruncateTableMixin, models.Model):
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, default=1, related_name='team_finance')
    period = models.SmallIntegerField(default=1)
    add_equity = models.IntegerField(default=1)
    dividend = models.SmallIntegerField(1)
    add_debt = models.IntegerField(default=1)


# Accounting
class GeneralLedgers(TruncateTableMixin, models.Model):
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, default=1,
                             related_name='team_general_ledger')
    period = models.SmallIntegerField(default=1)
    comment = models.CharField(max_length=256, default='', blank=True, null=True)

    def __str__(self):
        return str(self.id) + " - " + str(self.team) + " - " + str(self.comment)


class GeneralLedgerDetail(TruncateTableMixin, models.Model):
    generalledger = models.ForeignKey(GeneralLedgers, on_delete=models.CASCADE, default=1,
                                      related_name='gl_general_ledger_detail')
    account = models.IntegerField(default=0, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    comment = models.CharField(max_length=256, default='', blank=True, null=True)

    def __str__(self):
        return str(self.account) + " - " + str(self.amount) + " - " + str(self.comment)


class TrialBalance(TruncateTableMixin, models.Model):
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, default=1, related_name='tb_general_ledger')
    period = models.SmallIntegerField(default=1)
    level = models.SmallIntegerField(default=0, blank=True, null=True)
    account = models.IntegerField(default=0, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.team)+"-"+str(self.period)+"-"+str(self.account)+": "+str(self.amount)+": "+str(self.level)
