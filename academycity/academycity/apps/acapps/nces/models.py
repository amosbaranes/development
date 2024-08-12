from __future__ import unicode_literals
from django.db import models

from academycity.apps.core.sql import TruncateTableMixin


class CountryDim(TruncateTableMixin, models.Model):
    country_name = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return str(self.country_name)


class RegionDim(TruncateTableMixin, models.Model):
    region_name = models.CharField(max_length=100, default='', blank=True, null=True)
    country_dim = models.ForeignKey(CountryDim, on_delete=models.CASCADE, default=1,
                                    related_name='country_dim_region_dim')

    def __str__(self):
        return str(self.region_name)


class DistrictDim(TruncateTableMixin, models.Model):
    district_name = models.CharField(max_length=40, default='', blank=True, null=True)
    region_dim = models.ForeignKey(RegionDim, on_delete=models.CASCADE, default=1,
                                   related_name='region_dim_district_dim')

    def __str__(self):
        return str(self.district_name) + "" + str(self.region_dim)


class MeasureDim(TruncateTableMixin, models.Model):
    measure_name = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return str(self.measure_name)


class TimeDim(TruncateTableMixin, models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    year = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.id)


class Fact(TruncateTableMixin, models.Model):
    time_dim = models.ForeignKey(TimeDim, on_delete=models.CASCADE, default=1,
                                 related_name='time_dim_fact')
    district_dim = models.ForeignKey(DistrictDim, on_delete=models.CASCADE, default=1,
                                     related_name='district_dim_fact')
    measure_dim = models.ForeignKey(MeasureDim, on_delete=models.CASCADE, default=1,
                                    related_name='measure_dim_fact')
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.var_dim) + " - " + str(self.entity_dim) + ": " + str(self.amount)

