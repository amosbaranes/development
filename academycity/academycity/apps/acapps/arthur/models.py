from __future__ import unicode_literals
from django.db import models
from academycity.apps.core.sql import TruncateTableMixin


class EntityDim(TruncateTableMixin, models.Model):
    entity_id = models.CharField(max_length=15, default='', blank=True, null=True)
    entity_serial = models.PositiveSmallIntegerField(default=0)
    entity_race = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.entity_id)


class MeasureGroupDim(TruncateTableMixin, models.Model):
    group_name = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return str(self.group_name)


class MeasureDim(TruncateTableMixin, models.Model):
    measure_name = models.CharField(max_length=100, default='', blank=True, null=True)
    measure_group_dim = models.ForeignKey(MeasureGroupDim, on_delete=models.CASCADE, default=1,
                                          related_name='measure_group_measures')
    measure_code = models.CharField(max_length=100, default='', blank=True, null=True)
    description = models.CharField(max_length=256, default='', blank=True, null=True)


    def __str__(self):
        return str(self.measure_name)


class Fact(TruncateTableMixin, models.Model):
    entity_dim = models.ForeignKey(EntityDim, on_delete=models.CASCADE, default=1,
                                    related_name='entity_dim_fact')
    measure_dim = models.ForeignKey(MeasureDim, on_delete=models.CASCADE, default=1,
                                    related_name='fact_measures')
    amount = models.DecimalField(max_digits=16, decimal_places=2, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.country_dim) + " - " + str(self.time_dim) + ": " + str(self.amount)

# ---------------------- Processed Data -------------------
class RangeDim(TruncateTableMixin, models.Model):
    range_name = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return str(self.range_name)

class RelImpFact(TruncateTableMixin, models.Model):
    range_dim = models.ForeignKey(RangeDim, on_delete=models.CASCADE, default=1,
                                 related_name='range_dim_relimp_fact')
    measure_dim = models.ForeignKey(MeasureDim, on_delete=models.CASCADE, default=1,
                                    related_name='measure_dim_relimp_fact')
    measure_group_dim = models.ForeignKey(MeasureGroupDim, on_delete=models.CASCADE, default=1,
                                          related_name='measure_group_dim_relimp_fact')
    amount = models.DecimalField(max_digits=16, decimal_places=2, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.range_dim) + " - " + str(self.measure_dim) + ": " + str(self.amount)

class OutputFact(TruncateTableMixin, models.Model):
    range_dim = models.ForeignKey(RangeDim, on_delete=models.CASCADE, default=1,
                                 related_name='range_dim_output_fact')
    entity_dim = models.ForeignKey(EntityDim, on_delete=models.CASCADE, default=1,
                                    related_name='entity_dim_output_fact')
    measure_dim = models.ForeignKey(MeasureDim, on_delete=models.CASCADE, default=1,
                                    related_name='measure_dim_output_fact')
    range_name = models.CharField(max_length=10, default='min', blank=True, null=True)
    amount = models.DecimalField(max_digits=16, decimal_places=2, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.range_dim) + " - " + str(self.entity_dim) + ": " + str(self.amount)

class MinMaxCut(TruncateTableMixin, models.Model):
    measure_dim = models.ForeignKey(MeasureDim, on_delete=models.CASCADE, default=1,
                                    related_name='measure_dim_min_max_cut')
    min = models.DecimalField(max_digits=24, decimal_places=10, default=0, blank=True, null=True)
    max = models.DecimalField(max_digits=24, decimal_places=10, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.measure_dim)+" min:"+str(self.min)+" max:"+str(self.max)