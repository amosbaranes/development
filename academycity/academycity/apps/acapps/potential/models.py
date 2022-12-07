from __future__ import unicode_literals
from django.db import models
from academycity.apps.core.sql import TruncateTableMixin


class PotentialWeb(TruncateTableMixin, models.Model):
    project_name = models.CharField(max_length=100, default='', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.project_name)


class TimeDim(TruncateTableMixin, models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    year = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.year)


class CountryDim(TruncateTableMixin, models.Model):
    country_name = models.CharField(max_length=100, default='', blank=True, null=True)
    country_code = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return str(self.country_code)


class MeasureGroupDim(TruncateTableMixin, models.Model):
    group_name = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return str(self.group_name)


class MeasureDim(TruncateTableMixin, models.Model):
    measure_name = models.CharField(max_length=100, default='', blank=True, null=True)
    measure_group_dim = models.ForeignKey(MeasureGroupDim, on_delete=models.CASCADE, default=1,
                                          related_name='country_dim_world_Bank_fact')
    measure_code = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return str(self.measure_name)


class MinMaxCut(TruncateTableMixin, models.Model):
    time_dim = models.ForeignKey(TimeDim, on_delete=models.CASCADE, default=1,
                                 related_name='time_dim_min_max_cut')
    measure_dim = models.ForeignKey(MeasureDim, on_delete=models.CASCADE, default=1,
                                    related_name='country_dim_min_max_cut')
    min = models.DecimalField(max_digits=16, decimal_places=6, default=0, blank=True, null=True)
    max = models.DecimalField(max_digits=16, decimal_places=6, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.time_dim)+" "+str(self.measure_dim)+" min:"+str(self.min)+" max:"+str(self.max)


class Fact(TruncateTableMixin, models.Model):
    time_dim = models.ForeignKey(TimeDim, on_delete=models.CASCADE, default=1,
                                 related_name='time_dim_world_Bank_fact')
    country_dim = models.ForeignKey(CountryDim, on_delete=models.CASCADE, default=1,
                                    related_name='country_dim_world_Bank_fact')
    measure_dim = models.ForeignKey(MeasureDim, on_delete=models.CASCADE, default=1,
                                    related_name='country_dim_world_Bank_fact')
    amount = models.DecimalField(max_digits=16, decimal_places=6, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.country_dim) + " - " + str(self.time_dim) + ": " + str(self.amount)
