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


class VitaminDim(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'vitamindim'
        verbose_name_plural = 'vitamindims'

    vitamin_name = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return str(self.food_name)


class VitaminFact(TruncateTableMixin, models.Model):
    vitamin_dim = models.ForeignKey(VitaminDim, on_delete=models.CASCADE, default=1,
                                    related_name='vitamin_dim_fact')
    food_dim = models.ForeignKey(FoodDim, on_delete=models.CASCADE, default=1,
                                 related_name='food_dim_fact')
    amount = models.DecimalField(max_digits=16, decimal_places=2, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.vitamin_dim) + " - " + str(self.food_dim) + ": " + str(self.amount)

