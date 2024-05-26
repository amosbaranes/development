from __future__ import unicode_literals
from django.db import models

from academycity.apps.core.sql import TruncateTableMixin


class VarGroupDim(TruncateTableMixin, models.Model):
    group_name = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return str(self.group_name)


class VarDim(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'vardim'
        verbose_name_plural = 'vardims'
        # ordering = ['-score']

    var_code = models.CharField(max_length=40, default='', blank=True, null=True)
    var_group_dim = models.ForeignKey(VarGroupDim, on_delete=models.CASCADE, default=1,
                                          related_name='var_dim_group_dim')
    score = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=True, null=True)
    count0 = models.SmallIntegerField(default=0, blank=True, null=True)
    count5 = models.SmallIntegerField(default=0, blank=True, null=True)
    count10 = models.SmallIntegerField(default=0, blank=True, null=True)
    count15 = models.SmallIntegerField(default=0, blank=True, null=True)
    count20 = models.SmallIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return str(self.var_code)+" : "+str(self.var_group_dim)


class EntityDim(TruncateTableMixin, models.Model):
    entity_code = models.CharField(max_length=40, default='', blank=True, null=True)

    def __str__(self):
        return str(self.entity_code)


class Fact(TruncateTableMixin, models.Model):
    var_dim = models.ForeignKey(VarDim, on_delete=models.CASCADE, default=1,
                                related_name='var_dim_fact')
    entity_dim = models.ForeignKey(EntityDim, on_delete=models.CASCADE, default=1,
                                   related_name='entity_dim_fact')
    amount = models.DecimalField(max_digits=10, decimal_places=4, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.var_dim) + " - " + str(self.entity_dim) + ": " + str(self.amount)


# --------- Temp Data for Min/Max -----------------
class Temp(TruncateTableMixin, models.Model):
    dep_var_dim = models.ForeignKey(VarDim, on_delete=models.CASCADE, default=1,
                                    related_name='dep_var_dim_temp_var')
    idx = models.IntegerField(default=0, blank=True, null=True)
    dic_hp = models.JSONField(null=True)

    def __str__(self):
        return str(self.dep_var_dim) +":"+ str(self.idx)

class TempVar(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'tempvar'
        verbose_name_plural = 'tempvars'
        # ordering = ['-amount']

    temp = models.ForeignKey(Temp, on_delete=models.CASCADE, default=1,
                             related_name='temp_vars')
    var_dim = models.ForeignKey(VarDim, on_delete=models.CASCADE, default=1,
                                related_name='var_dim_temp_var')
    sign = models.SmallIntegerField(default=1, blank=True, null=True)
    amount = models.DecimalField(max_digits=4, decimal_places=2, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.temp)
# -------------------------------------------------

# --------------
class FactNormalizedMinMax(TruncateTableMixin, models.Model):
    var_dim = models.ForeignKey(VarDim, on_delete=models.CASCADE, default=1,
                                 related_name='var_dim_fact_normalized_minmax')
    entity_dim = models.ForeignKey(EntityDim, on_delete=models.CASCADE, default=1,
                                   related_name='entity_dim_fact_normalized_minmax')
    amount = models.DecimalField(max_digits=10, decimal_places=4, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.gene_dim) + " - " + str(self.person_dim) + ": " + str(self.amount)
# --------------