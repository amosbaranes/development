from __future__ import unicode_literals
from django.db import models
from academycity.apps.core.sql import TruncateTableMixin

class FoodGroupDim(TruncateTableMixin, models.Model):
    group_name = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return str(self.group_name)


class FoodDim(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'fooddim'
        verbose_name_plural = 'fooddims'

    group_name = models.ForeignKey(FoodGroupDim, on_delete=models.CASCADE, default=1,
                                          related_name='food_dim_group_dim')
    food_name = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return str(self.food_name)

