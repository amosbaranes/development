from __future__ import unicode_literals
from django.db import models
from academycity.apps.core.sql import TruncateTableMixin


class GeneDim(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'gendim'
        verbose_name_plural = 'gendims'
        ordering = ['gene_code']

    gene_code = models.CharField(max_length=40, default='', blank=True, null=True)
    clusters = models.JSONField(null=True)
    reduced_clusters = models.JSONField(null=True)

    def __str__(self):
        return str(self.gene_code)


class PersonDim(TruncateTableMixin, models.Model):
    gender = models.SmallIntegerField(default=0, blank=True, null=True)
    person_code = models.CharField(max_length=40, default='', blank=True, null=True)
    age_at_cdna = models.SmallIntegerField(blank=True, null=True)
    set_num = models.SmallIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.person_code)


class Fact(TruncateTableMixin, models.Model):
    gene_dim = models.ForeignKey(GeneDim, on_delete=models.CASCADE, default=1,
                                 related_name='gene_dim_fact')
    person_dim = models.ForeignKey(PersonDim, on_delete=models.CASCADE, default=1,
                                   related_name='person_dim_fact')
    amount = models.DecimalField(max_digits=10, decimal_places=4, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.gene_dim) + " - " + str(self.person_dim) + ": " + str(self.amount)


# --------- For Analysis ------------------------------
class FactNormalized(TruncateTableMixin, models.Model):
    gene_dim = models.ForeignKey(GeneDim, on_delete=models.CASCADE, default=1,
                                 related_name='gene_dim_fact_normalized')
    person_dim = models.ForeignKey(PersonDim, on_delete=models.CASCADE, default=1,
                                   related_name='person_dim_fact_normalized')
    amount = models.DecimalField(max_digits=10, decimal_places=4, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.gene_dim) + " - " + str(self.person_dim) + ": " + str(self.amount)

