from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _, get_language
from academycity.apps.core.sql import TruncateTableMixin

class GeneGroupDim(TruncateTableMixin, models.Model):
    group_name = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return str(self.group_name)


class GeneDim(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'gendim'
        verbose_name_plural = 'gendims'
        # ordering = ['-score']

    gene_code = models.CharField(max_length=40, default='', blank=True, null=True)
    gene_group_dim = models.ForeignKey(GeneGroupDim, on_delete=models.CASCADE, default=1,
                                          related_name='gene_dim_group_dim')
    clusters = models.JSONField(null=True)
    reduced_clusters = models.JSONField(null=True)
    score = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=True, null=True)
    count0 = models.SmallIntegerField(default=0, blank=True, null=True)
    count5 = models.SmallIntegerField(default=0, blank=True, null=True)
    count10 = models.SmallIntegerField(default=0, blank=True, null=True)
    count15 = models.SmallIntegerField(default=0, blank=True, null=True)
    count20 = models.SmallIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return str(self.gene_code)


class PersonGroupDim(TruncateTableMixin, models.Model):
    group_name = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return str(self.group_name)


class PersonDim(TruncateTableMixin, models.Model):
    person_group_dim = models.ForeignKey(PersonGroupDim, on_delete=models.CASCADE, default=1,
                                         related_name='person_dim_group_dim')
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

# --------- Temp Data for Min/Max ----------------
class Temp(TruncateTableMixin, models.Model):
    idx = models.IntegerField(default=0, blank=True, null=True)
    dic_hp = models.JSONField(null=True)

    def __str__(self):
        return str(self.idx)

class TempVar(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'tempvar'
        verbose_name_plural = 'tempvars'
        # ordering = ['-amount']

    temp = models.ForeignKey(Temp, on_delete=models.CASCADE, default=1,
                             related_name='temp_vars')
    # var = models.SmallIntegerField(default=0, blank=True, null=True)
    gene_dim = models.ForeignKey(GeneDim, on_delete=models.CASCADE, default=1,
                                 related_name='gene_dim_temp_var')
    sign = models.SmallIntegerField(default=1, blank=True, null=True)
    amount = models.DecimalField(max_digits=4, decimal_places=2, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.temp)
# -------------------------------------------------

# --------- For Analysis for Batch normalization ---------
class FactNormalizedTemp(TruncateTableMixin, models.Model):
    gene_dim = models.ForeignKey(GeneDim, on_delete=models.CASCADE, default=1,
                                 related_name='gene_dim_fact_normalized_temp')
    person_dim = models.ForeignKey(PersonDim, on_delete=models.CASCADE, default=1,
                                   related_name='person_dim_fact_normalized_temp')
    amount = models.DecimalField(max_digits=10, decimal_places=4, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.gene_dim) + " - " + str(self.person_dim) + ": " + str(self.amount)


class FactNormalized(TruncateTableMixin, models.Model):
    gene_dim = models.ForeignKey(GeneDim, on_delete=models.CASCADE, default=1,
                                 related_name='gene_dim_fact_normalized')
    person_dim = models.ForeignKey(PersonDim, on_delete=models.CASCADE, default=1,
                                   related_name='person_dim_fact_normalized')
    amount = models.DecimalField(max_digits=10, decimal_places=4, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.gene_dim) + " - " + str(self.person_dim) + ": " + str(self.amount)


class PCA(TruncateTableMixin, models.Model):

    class Meta:
        verbose_name = _('pca')
        verbose_name_plural = _('pcas')
        ordering = ['set','sub_set','component']
    #
    set = models.SmallIntegerField(blank=True, null=True)
    sub_set = models.SmallIntegerField(blank=True, null=True)
    component = models.SmallIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.set) + " - " + str(self.sub_set) + ": " + str(self.component)

class PCAData(TruncateTableMixin, models.Model):

    class Meta:
        verbose_name = _('pcadata')
        verbose_name_plural = _('pcadatas')
        ordering = ['pca','idx']
    #
    pca = models.ForeignKey(PCA, on_delete=models.CASCADE, default=1, related_name='pca_pca_data')
    idx = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=4, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.pca) + " - " + str(self.idx)

# --------------------------------------------------------


class Debug(TruncateTableMixin, models.Model):
    value = models.CharField(max_length=1024)

    def __str__(self):
        return self.value
