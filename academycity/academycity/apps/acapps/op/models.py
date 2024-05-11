from __future__ import unicode_literals
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.db import models
# from django.utils.encoding import python_2_unicode_compatible, force_text
from django.utils.translation import ugettext_lazy as _, get_language

from filer.fields.image import FilerImageField
from cms.models.fields import PlaceholderField
from parler.models import TranslatableModel, TranslatedFields
from django.core.validators import MinValueValidator, MaxValueValidator
from parler.utils.context import switch_language
from django.utils.text import slugify
import math
from django.db import connection
from cms.models.pluginmodel import CMSPlugin

from ...core.sql import TruncateTableMixin
import decimal
import datetime
from datetime import timedelta

from django.db.models.functions import Coalesce
from scipy.stats import pearsonr
from ...core.utils import log_debug


class CompanyInfo(TruncateTableMixin, models.Model):

    class Meta:
        verbose_name = _('Company Info')
        verbose_name_plural = _('Companies Info')
        ordering = ['company_name']
    #
    company_name = models.CharField(max_length=128, default='', blank=True, null=True)
    ticker = models.CharField(max_length=10, null=False)

    def __str__(self):
        return str(self.company_name) + " : " + str(self.ticker)


class StockPricesDays(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('StockPricesDay')
        verbose_name_plural = _('StockPricesDays')
        ordering = ['company__id', '-idx']

    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, default=None, blank=True, null=True,
                                related_name='company_info_stock_prices_days')
    idx = models.PositiveBigIntegerField(default=0)
    open = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    high = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    low = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    close = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    volume = models.PositiveIntegerField(default=0)
    dividends = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    stock_splits = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return str(self.idx)


class StockReturnStd(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('StockReturnStd')
        verbose_name_plural = _('StockReturnStds')
        ordering = ['company__id', 'idx']

    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, default=None, blank=True, null=True,
                                related_name='company_stock_return_std')
    idx = models.PositiveBigIntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=6, default=0)

    def __str__(self):
        return str(self.idx) + ": " +str(self.company)

