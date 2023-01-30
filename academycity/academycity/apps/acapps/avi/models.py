from __future__ import unicode_literals
from django.db import models
from academycity.apps.core.sql import TruncateTableMixin


class TimeDim(TruncateTableMixin, models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    year = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.id)


class CountryDim(TruncateTableMixin, models.Model):
    country_name = models.CharField(max_length=100, default='', blank=True, null=True)
    country_code = models.CharField(max_length=100, default='', blank=True, null=True)
    country_cc = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return str(self.country_name)


class UniversityDim(TruncateTableMixin, models.Model):
    country_dim = models.ForeignKey(CountryDim, on_delete=models.CASCADE, default=1,
                                          related_name='country_dim_university')
    university_name = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return str(self.university_name)


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


class WorldBankFact(TruncateTableMixin, models.Model):
    time_dim = models.ForeignKey(TimeDim, on_delete=models.CASCADE, default=1,
                                 related_name='time_dim_world_Bank_fact')
    country_dim = models.ForeignKey(CountryDim, on_delete=models.CASCADE, default=1,
                                    related_name='country_dim_world_Bank_fact')
    measure_dim = models.ForeignKey(MeasureDim, on_delete=models.CASCADE, default=1,
                                    related_name='measure_dim_world_Bank_fact')
    amount = models.DecimalField(max_digits=16, decimal_places=2, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.country_dim) + " - " + str(self.time_dim) + ": " + str(self.amount)


class UniversityRankFact(TruncateTableMixin, models.Model):
    time_dim = models.ForeignKey(TimeDim, on_delete=models.CASCADE, default=1,
                                 related_name='time_dim_university_rank_fact')
    country_dim = models.ForeignKey(CountryDim, on_delete=models.CASCADE, default=1,
                                    related_name='country_dim_university_rank_fact')
    university_dim = models.ForeignKey(UniversityDim, on_delete=models.CASCADE, default=1,
                                    related_name='university_dim_university_rank_fact')
    measure_dim = models.ForeignKey(MeasureDim, on_delete=models.CASCADE, default=1,
                                    related_name='measure_dim_university_rank_fact')
    amount = models.DecimalField(max_digits=16, decimal_places=2, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.country_dim) + " - " + str(self.time_dim) + ": " + str(self.amount)


class MinMaxCut(TruncateTableMixin, models.Model):
    time_dim = models.ForeignKey(TimeDim, on_delete=models.CASCADE, default=1,
                                 related_name='time_dim_min_max_cut')
    measure_dim = models.ForeignKey(MeasureDim, on_delete=models.CASCADE, default=1,
                                    related_name='country_dim_min_max_cut')
    min = models.DecimalField(max_digits=18, decimal_places=6, default=0, blank=True, null=True)
    max = models.DecimalField(max_digits=18, decimal_places=6, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.time_dim)+" "+str(self.measure_dim)+" min:"+str(self.min)+" max:"+str(self.max)