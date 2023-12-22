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

from ..courses.models import (CourseSchedule, CourseScheduleUser, Team)
from ..core.sql import TruncateTableMixin
import decimal
import datetime
from datetime import timedelta

from django.db.models.functions import Coalesce
from scipy.stats import pearsonr
from ..core.utils import log_debug


# Data
# RBOIC = RatingBasedOnInterestCavrage
class RBOIC(TruncateTableMixin, models.Model):
    from_ic = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    to_ic = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    rating = models.CharField(max_length=100, default='')
    spread = models.DecimalField(max_digits=18, decimal_places=6, default=0.0)


class CountryRegion(TruncateTableMixin, models.Model):
    pkey_region = models.AutoField(primary_key=True)
    region = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.region


# To Be deleted
class CountryRating(TruncateTableMixin, models.Model):
    pkey_country_rating = models.AutoField(primary_key=True, default=None)
    country_rating = models.CharField(max_length=4, default='', blank=True, null=True)
    default_spread = models.DecimalField(max_digits=18, decimal_places=6, default=1)

    def __str__(self):
        return self.country_rating + ': ' + str(self.default_spread)


# To Be deleted
class Country(TruncateTableMixin, models.Model):
    country = models.CharField(max_length=50, default='', blank=True, null=True)
    marginal_tax_rate = models.DecimalField(max_digits=18, decimal_places=6, default=1)
    long_term_rating = models.ForeignKey(CountryRating, on_delete=models.SET_NULL, null=True,
                                         related_name='rating_countries')
    region = models.ForeignKey(CountryRegion, default=0, on_delete=models.CASCADE,
                               related_name='region_countries')

    @property
    def adj_default_spread(self):
        return self.long_term_rating.default_spread

    @property
    def country_risk_premium(self):
        return self.long_term_rating.default_spread * Project.objects.last().volatility_ratio

    @property
    def total_risk_premium(self):
        p = Project.objects.last()
        return self.long_term_rating.default_spread * p.volatility_ratio + p.mature_marker_risk_premium

    def __str__(self):
        return self.country


# To Be deleted
class GlobalIndustryAverages(TruncateTableMixin, models.Model):
    industry_name = models.CharField(max_length=50, default='', blank=True, null=True)
    number_of_firms = models.PositiveIntegerField(default=1)
    unlevered_beta_corrected_for_cash = models.DecimalField(max_digits=7, decimal_places=4, default=1)
    market_d_over_e_ratio = models.DecimalField(max_digits=7, decimal_places=4, default=1)
    market_debt_to_capital = models.DecimalField(max_digits=7, decimal_places=4, default=1)
    effective_tax_rate = models.DecimalField(max_digits=7, decimal_places=4, default=1)
    dividend_payout = models.DecimalField(max_digits=7, decimal_places=4, default=1)
    net_margin = models.DecimalField(max_digits=7, decimal_places=4, default=1)
    pre_tax_operating_margin = models.DecimalField(max_digits=7, decimal_places=4, default=1)
    roe = models.DecimalField(max_digits=7, decimal_places=4, default=1)
    roic = models.DecimalField(max_digits=7, decimal_places=4, default=1)
    SalesOverCapital = models.DecimalField(max_digits=7, decimal_places=4, default=1)
    ev_over_sales = models.DecimalField(max_digits=7, decimal_places=4, default=1)
    revenue_growth_rateLast_5_years = models.DecimalField(max_digits=7, decimal_places=4, default=1)
    expected_earnings_growth_next_5_years = models.DecimalField(max_digits=7, decimal_places=4, default=1)

    def __str__(self):
        return self.industry_name


# To Be deleted
class Industry(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('Industry')
        verbose_name_plural = _('Industry')
        ordering = ['sic_code']

    sic_code = models.SmallIntegerField(primary_key=True)
    sic_description = models.CharField(max_length=128, default='', blank=True, null=True)

    def __str__(self):
        return str(self.sic_code) + ': ' + str(self.sic_description)


class CompanyInfo(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('Company Info')
        verbose_name_plural = _('Company Info')
        ordering = ['company_name']
    #
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, default=None, blank=True, null=True)
    ticker = models.CharField(max_length=10, null=False)
    cik = models.CharField(max_length=10, null=True)
    company_name = models.CharField(max_length=128, default='', blank=True, null=True)
    #
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    zip = models.CharField(max_length=10, null=True)
    #
    # industry = models.ForeignKey(GlobalIndustryAverages, on_delete=models.CASCADE, default=None)
    # country = models.ForeignKey(Country, on_delete=models.CASCADE, default=None)

    #
    def __str__(self):
        return self.company_name


class CompanyData(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('Company Data')
        verbose_name_plural = _('Company Data')
        ordering = ['company', 'year']

    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, default=None,
                                related_name='company_data')
    year = models.SmallIntegerField(default=2018)
    ebit = models.DecimalField(max_digits=18, decimal_places=0, default=0) # operating income
    number_of_shares = models.BigIntegerField(default=0)
    share_price = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    cash_cash_equivalents = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    preferred_stock = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    market_value_equity = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    noncurrent_liabilities = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    long_term_debt_noncurrent = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    equity_attributable_to_oncontrolling_interest = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    revenue = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    interest_expense = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    #
    income_taxes = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    effective_tax_rate = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    interest_coverage_ratio = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    total_long_term_debt = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    intangible_assets_net = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    goodwill = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    enterprise_value = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    ev_over_revenue = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    ebitda = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    p_over_e_ratio = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    p_over_s_ratio = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    p_over_b_ratio = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    p_over_cash_flow_ratio = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    p_over_ebitda_ratio = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    stockholders_equity = models.DecimalField(max_digits=18, decimal_places=0, default=0)

#  noncurrent_liabilities+stockholders_equity
# class CompanyValuation(models.Model):
#     class Meta:
#         verbose_name = _('Company Valuation')
#         verbose_name_plural = _('Company Valuation')
#         ordering = ['company', 'year']
#
#     company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, default=None,
#                                 related_name='company_valuation')
#     year = models.SmallIntegerField(default=2018) # year of valuation

    # equity =  models.DecimalField(max_digits=18, decimal_places=0, default=0) # stockholder equity
    # debt = models.DecimalField(max_digits=18, decimal_places=0, default=0) # noncurrent_liabilities
    # cofd = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    # cofe = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    # wacc = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    # mtr = models.DecimalField(max_digits=18, decimal_places=0, default=0) # marginal tax rate

    # etr = models.DecimalField(max_digits=18, decimal_places=0, default=0) # effective tax rate

    # mature_marker_risk_premium = models.DecimalField(max_digits=8, decimal_places=4, default=0.0525)
    # rf = models.DecimalField(max_digits=8, decimal_places=4, default=0.02)
    #
    # stg = models.DecimalField(max_digits=18, decimal_places=0, default=0) # short term growth
    # stroic = models.DecimalField(max_digits=18, decimal_places=0, default=0) # short term roic
    # strir = models.DecimalField(max_digits=18, decimal_places=0, default=0) # short term reinvestment rate

    #ltg = models.DecimalField(max_digits=18, decimal_places=0, default=0) # long term growth
    #ltroic = models.DecimalField(max_digits=18, decimal_places=0, default=0) # long term roic
    #ltrir = models.DecimalField(max_digits=18, decimal_places=0, default=0) # long term rir

    # pv = models.DecimalField(max_digits=18, decimal_places=0, default=0)

    # minority = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    # preferedstock = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    # excesscash = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    # # ivps = models.DecimalField(max_digits=18, decimal_places=0, default=0) # iv per share
    # nofs = models.SmallIntegerField(default=5) # number of shares
    # mpps = models.DecimalField(max_digits=18, decimal_places=0, default=0) # market price per share

    #
    snofy = models.SmallIntegerField(default=5) # short number of years of growth
    nofy_for_roic_et = models.SmallIntegerField(default=3) # number of years for roic and effective tax rate
    #
    @property
    def debt(self):
        return self.noncurrent_liabilities

    @property
    def equity(self):
        return self.stockholders_equity

    @property
    def d_over_e(self):
        if abs(self.equity) < 0.1:
            return 1    # need to fix
        return self.debt / self.equity

    # defined above
    @property
    def interest_coverage_ratio_calculated(self):
        if abs(float(self.interest_expense)) < 1:
            icr = self.interest_coverage_ratio     # need to fix
        else:
            icr = self.ebit / self.interest_expense
        return icr

    @property
    def company_default_spread(self):
        icr = self.interest_coverage_ratio
        o = RBOIC.objects.filter(to_ic__gte=icr).filter(from_ic__lte=icr).all()[0]
        return o.spread

    # need to modified the project table by by year
    @property
    def project(self):
        return Project.objects.last()

    @property
    def mature_marker_risk_premium(self):
        return self.project.mature_marker_risk_premium

    @property
    def rf(self):
        return self.project.rf

    @property
    def county(self):
        return Country.objects.get(country="United States")

    @property
    def country_spread(self):
        return self.county.adj_default_spread

    @property
    def country_risk_premium(self):
        return self.county.country_risk_premium

    @property
    def country_tax_rate(self):
        return self.county.marginal_tax_rate

    @property
    def cost_of_debt(self):
        return self.rf + 1*self.company_default_spread + 1 * self.country_spread

    @property
    def unleveraged_beta(self):
        unleverged_beta_ = 1.0    # need to change
        return unleverged_beta_

    @property
    def leveraged_beta(self):
        leverged_beta_ = self.unleveraged_beta *  (1 + (1 - float(self.country_tax_rate)) * float(self.d_over_e))
        return leverged_beta_

    @property
    def cost_of_equity(self):
        return float(self.rf) + float(self.leveraged_beta) * (1*float(self.company_default_spread) + 1 * float(self.mature_marker_risk_premium))

    @property
    def wacc(self):
        e_over_v = float(1/(self.d_over_e + 1))
        d_over_v = 1 - e_over_v
        wacc = float(d_over_v) * float(self.cost_of_debt) * (1 - 1 * float(self.country_tax_rate)) + e_over_v * float(self.cost_of_equity)
        return wacc

    @property
    def effective_tax_rate_based_on_n_years(self):
        from_year = self.year - self.nofy_for_roic_et + 1
        cds = CompanyData.objects.filter(company=self.company, year__gte=from_year)
        tax = 0
        ebit =0
        for cd in cds:
            tax += cd.income_taxes
            ebit += cd.ebit
        if abs(ebit) <1:
            return -999
        return tax/ebit

    @property
    def short_term_growth(self):
        return 0.05    # need to change

    @property
    def short_term_roic_based_on_n_years(self):
        from_year = self.year - self.nofy_for_roic_et +1
        cds = CompanyData.objects.filter(company=self.company, year__gte=from_year)
        nebit =0
        d_e = 0
        for cd in cds:
            nebit += (cd.ebit - cd.income_taxes)
            d_e += (cd.noncurrent_liabilities + cd.stockholders_equity)
        if abs(d_e) <1:
            return -999 # need to fix
        return nebit/d_e    # need to change

    @property
    def short_term_reinvestment_rate(self):
        try:
            nn = float(self.short_term_growth)/float(self.short_term_roic_based_on_n_years)
        except Exception as ex:
            nn = float("NaN")
        return nn  # need to complete

    @property
    def long_term_growth(self):
        return 0.02  # need to complete

    @property
    def long_term_roic(self):
        return self.wacc

    @property
    def long_term_reinvestment_rate(self):
        return float(self.long_term_growth)/float(self.long_term_roic)  # need to complete

    @property
    def minority(self):
        return self.equity_attributable_to_oncontrolling_interest

    @property
    def excess_cash(self):
        return 0  # need to fix this

    @property
    def pvm(self):
        return self.pv/1000000

    @property
    def pv(self):
        pv = 0
        df = 1/(1 + self.wacc)
        for j in range(1, 1 * self.snofy + 1):
            cfj = float(self.ebit) * float(math.pow(1 + self.short_term_growth, j))
            fcfj = cfj * (1 - float(self.effective_tax_rate)) * (1 - float(self.short_term_reinvestment_rate))
            pv += fcfj * math.pow(df, j)
            if j == self.snofy:
                cfj = float(self.ebit) * math.pow(1 + float(self.short_term_growth), self.snofy)
                cfj_ss = cfj * (1 + float(self.long_term_growth)) * (1-float(self.country_tax_rate)) * (1-float(self.long_term_reinvestment_rate))
                tv_ = cfj_ss * math.pow(df, j) / (float(self.wacc) - float(self.long_term_growth))
                pv += tv_
        return pv

    @property
    def iv_per_share(self):
        iv = float(self.pv) - float(self.debt) - float(self.minority) - float(self.preferred_stock) + float(self.excess_cash)
        if abs(self.number_of_shares) < 1:
            return "missing data"
        iv_per_share = iv / self.number_of_shares
        return iv_per_share


class Project(TruncateTableMixin, TranslatableModel):
    STATUS = (
        (0, 'Created'),
        (5, 'Approved'),
        (30, 'Running'),
        (100, 'Finished')
    )

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')
        ordering = ['-id']

    id = models.AutoField(primary_key=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    status = models.IntegerField(default=0, choices=STATUS)
    year = models.PositiveSmallIntegerField(default=2020)
    quarter = models.PositiveSmallIntegerField(default=4)
    #
    course_schedule = models.OneToOneField(CourseSchedule, on_delete=models.CASCADE, null=True, related_name='project')
    description = PlaceholderField('project_description')
    image = FilerImageField(blank=True, null=True, on_delete=models.SET_NULL)
    #
    mature_marker_risk_premium = models.DecimalField(max_digits=8, decimal_places=4, default=0.0525)
    volatility_ratio = models.DecimalField(max_digits=8, decimal_places=4, default=1.50)
    rf = models.DecimalField(max_digits=8, decimal_places=4, default=0.02)
    #
    dic_data = models.JSONField(null=True)   # relate to risk premium
    #

    translations = TranslatedFields(
        name=models.CharField(_('name'), blank=False, default='',
                              help_text=_('Please supply the project name.'), max_length=128),
        slug=models.SlugField(_('slug'), blank=True, default='',
                              help_text=_('Please supply the project slug.'), max_length=128)
    )

    # def get_absolute_url(self):
    #     with switch_language(self, get_language()):
    #         return reverse('corporatevaluation:project_detail', kwargs={'slug': self.slug, })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.id) + '-' + self.course_schedule.name + '-' + self.name + ' ' + get_language())
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Valuation(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('Valuation')
        verbose_name_plural = _('Valuations')
        ordering = ['user', 'company_info']

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE,
                             related_name='user_valuations')
    company_info = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, default=None, blank=True, null=True)


class XBRLMainIndustryInfo(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRLMainIndustry')
        verbose_name_plural = _('XBRLMainIndustries')
        ordering = ['sic_code']
    sic_code = models.PositiveSmallIntegerField(primary_key=True)
    sic_description = models.CharField(max_length=128, default='', blank=True, null=True)

    def __str__(self):
        return str(self.sic_code) + ': ' + str(self.sic_description)


class XBRLIndustryInfo(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRLIndustry')
        verbose_name_plural = _('XBRLIndustries')
        ordering = ['sic_description']
    #
    sic_code = models.PositiveSmallIntegerField(primary_key=True)
    main_sic = models.ForeignKey(XBRLMainIndustryInfo, on_delete=models.CASCADE, default=None, blank=True, null=True)
    sic_description = models.CharField(max_length=128, default='', blank=True, null=True)
    #
    industry_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.sic_code) + ': ' + str(self.sic_description)


class XBRLCompanyInfoInProcess(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRLCompanyInfoInProcess')
        verbose_name_plural = _('XBRLCompanyInfoInProcesses')
        ordering = ['company_name']
    #
    exchange = models.CharField(max_length=10, default='nyse')
    company_name = models.CharField(max_length=128, default='', blank=True, null=True)
    ticker = models.CharField(max_length=10, null=False)
    company_letter = models.CharField(max_length=1, default='')

    cik = models.CharField(max_length=10, null=True)
    sic = models.PositiveSmallIntegerField(default=0)
    is_error = models.BooleanField(default=False)
    message = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.company_name

# https://docs.djangoproject.com/en/3.2/topics/db/managers/
# class XBRLRegionQuerySet(models.QuerySet):
#     def averages(self):
#         return self.filter(countries__country_data__year=XBRLCountryYearData.project.year)\
#             .annotate(num_countries=Coalesce(models.Avg("countries__country_data__tax_rate"), 0))


class XBRLRegion(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRL Region')
        verbose_name_plural = _('XBRL Regions')
        ordering = ['name']
    #
    name = models.CharField(max_length=128, default='', blank=True, null=True)
    full_name = models.CharField(max_length=128, default='', blank=True, null=True)
    updated_adamodar = models.BooleanField(default=False)

    # objects = models.Manager()  # The default manager.
    # region_objects = XBRLRegionQuerySet.as_manager()  # The project manager.

    def __str__(self):
        return str(self.full_name) + " (" + str(self.name) + ")"


class XBRLCountry(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRL Country')
        verbose_name_plural = _('XBRL Countries')
        ordering = ['name']
    #
    region = models.ForeignKey(XBRLRegion, on_delete=models.CASCADE, default=None, blank=True, null=True,
                               related_name='countries')
    name = models.CharField(max_length=128, default='', blank=True, null=True)
    updated_adamodar = models.BooleanField(default=False)
    #
    iso_2 = models.CharField(max_length=2, default='')
    iso_3 = models.CharField(max_length=3, default='')
    oecd = models.BooleanField(default=False)
    eu27 = models.BooleanField(default=False)
    gseven = models.BooleanField(default=False)
    gtwenty = models.BooleanField(default=False)
    brics = models.BooleanField(default=False)

    def __str__(self):
        if self.region:
            return str(self.name) + " (" + str(self.region.name) + ")"
        else:
            return str(self.name)


class XBRLCountryYearDataProject(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(year=self.model.project.year)


class XBRLSPMoodys(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRLSPMoodys')
        verbose_name_plural = _('XBRLSPMoodys')
        ordering = ['-year']
    #
    year = models.PositiveSmallIntegerField(default=0)
    sp = models.CharField(max_length=10, default='')
    moodys = models.CharField(max_length=10, default='')
    default_spread = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    score_from = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, default=0)
    score_to = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, default=0)

    def __str__(self):
        return str(self.sp) + " = " + str(self.moodys) + " default_spread: " + str(self.default_spread) + \
               " score_from: " + str(self.score_from) + " score_to: " + str(self.score_to)


class XBRLRegionYearData(TruncateTableMixin, models.Model):
    project = None

    class Meta:
        verbose_name = _('XBRL Region Year Data')
        verbose_name_plural = _('XBRL Regions Year Data')
        ordering = ['region', 'year']

    region = models.ForeignKey(XBRLRegion, on_delete=models.CASCADE, default=None, blank=True, null=True,
                               related_name='region_data')
    year = models.PositiveSmallIntegerField(default=0)
    # The following are dimensions
    tax_rate = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    moodys_rate_completed_by_sp = models.CharField(max_length=20, default='NA')
    rating_based_default_spread = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    country_risk_premium_rating = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    # Managers
    objects = models.Manager()  # The default manager.
    project_objects = XBRLCountryYearDataProject()  # The project manager.


#
class ETFS(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('ETFS')
        verbose_name_plural = _('ETFS')
        ordering = ['symbol']

    symbol = models.CharField(max_length=5, default='', blank=True, null=True)
    description = models.CharField(max_length=128, default='', blank=True, null=True)

    def __str__(self):
        return str(self.symbol) + ': ' + str(self.description)


class ETFWatchLists(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('ETFWatchLists')
        verbose_name_plural = _('ETFWatchLists')
        ordering = ['symbol']

    symbol = models.CharField(max_length=5, default='', blank=True, null=True)
    description = models.CharField(max_length=128, default='', blank=True, null=True)

    def __str__(self):
        return str(self.symbol) + ': ' + str(self.description)


class XBRLCompanyInfo(TruncateTableMixin, models.Model):

    class Meta:
        verbose_name = _('XBRL Company Info')
        verbose_name_plural = _('XBRL Companies Info')
        ordering = ['company_name']
    #
    industry = models.ForeignKey(XBRLIndustryInfo, on_delete=models.CASCADE, default=None, blank=True, null=True)
    country_of_incorporation = models.ForeignKey(XBRLCountry, on_delete=models.CASCADE, default=None, blank=True,
                                                 null=True, related_name="country_companies")
    etf = models.ForeignKey(ETFS, on_delete=models.CASCADE, default=None, blank=True, null=True,
                            related_name="eft_xbrlcompanyinfo")
    etfwatchlist = models.ForeignKey(ETFWatchLists, on_delete=models.CASCADE, default=None, blank=True, null=True,
                            related_name="etf_watch_list_xbrlcompanyinfo")
    exchange = models.CharField(max_length=10, default='nyse')
    company_name = models.CharField(max_length=128, default='', blank=True, null=True)
    ticker = models.CharField(max_length=10, null=False)
    company_letter = models.CharField(max_length=1, default='')
    cik = models.CharField(max_length=10, null=True)
    is_active = models.BooleanField(default=False)
    #
    financial_data = models.JSONField(null=True)
    financial_dataq = models.JSONField(null=True)
    #
    company_description = models.TextField(blank=True, null=True)
    #
    city = models.CharField(max_length=50, default="", blank=True)
    state = models.CharField(max_length=50, default="", blank=True)
    zip = models.CharField(max_length=10, default="", blank=True)
    #
    by_country_or_regine = models.BooleanField(default=True)

    @property
    def tax_rate(self):
        try:
            if not self.country_of_incorporation:
                # print('-6'*50)
                self.country_of_incorporation = XBRLCountry.objects.get(name="United States")
                self.save()
                # print('-7'*50)
                log_debug("You need to setup country_of_incorporation: default is United States of America.")
            t_ = XBRLCountryYearData.project_objects.get(country=self.country_of_incorporation).tax_rate
        except Exception as ex:
            print("Error: you need to setup country_of_incorporation:" + str(ex))
            return 0.0
            # log_debug("Error: you need to setup country_of_incorporation:" + str(ex))
        return t_

    def get_countries_regions(self):
        # log_debug("get_countries_regions 0")
        dic = {}
        try:
            log_debug("get_countries_regions 1")
            for y in self.years_of_operation.all():
                # log_debug("get_countries_regions year: " + str(y))
                # log_debug("get_countries_regions 1")
                dic[y.year] = {}
                dic[y.year]['countries'] = {}
                for c in y.countries_of_operation.all():
                    dic[y.year]['countries'][c.country.id] = [str(c.id), str(c.revenues), str(c.rating), str(c.spread),
                                                              str(c.risk_premium), str(c.tax_rate)]
                # log_debug("get_countries_regions 2")
                dic[y.year]['regions'] = {}
                for r in y.regions_of_operation.all():
                    dic[y.year]['regions'][r.region.id] = [str(r.id), str(r.revenues), str(r.rating), str(r.spread),
                                                           str(r.risk_premium), str(r.tax_rate)]
                # log_debug("get_countries_regions 3")
                dic[y.year]['industries'] = {}
                for r in y.industries_of_operation.all():
                    dic[y.year]['industries'][r.industry.id] = [str(r.id), str(r.revenues), str(r.ev_over_sales),
                                                                str(r.estimated_value), str(r.unlevered_beta),
                                                                str(r.estimated_growth)]
                # log_debug("get_countries_regions 4")
            # log_debug("get_countries_regions 10")
        except Exception as ex:
            log_debug("get_countries_regions ex: " + str(ex))
            print(dic)
        # log_debug("get_countries_regions 11")
        return dic

    def __str__(self):
        return str(self.company_name) + " : " + str(self.ticker)


class CompaniesPriceData(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('CompaniesPriceData')
        verbose_name_plural = _('CompaniesPriceData')
        ordering = ['company']

    company = models.ForeignKey(XBRLCompanyInfo, on_delete=models.CASCADE, default=None, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    close_price = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    def __str__(self):
        return str(self.company) + ' : ' + str(self.date) + ' : ' + str(self.close_price)
#

class XBRLHistoricalReturnsSP(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRLHistoricalReturnsSP')
        verbose_name_plural = _('XBRLHistoricalReturnsSP')
        ordering = ['-year']
    #
    year = models.PositiveSmallIntegerField(default=0)
    aaa = models.DecimalField(max_digits=8, decimal_places=4, default=None, blank=True, null=True)
    bbb = models.DecimalField(max_digits=8, decimal_places=4, default=None, blank=True, null=True)
    tb3ms = models.DecimalField(max_digits=8, decimal_places=4, default=None, blank=True, null=True)
    tb10y = models.DecimalField(max_digits=8, decimal_places=4, default=None, blank=True, null=True)
    sp500 = models.DecimalField(max_digits=8, decimal_places=2, default=None, blank=True, null=True)
    dividend_yield = models.DecimalField(max_digits=8, decimal_places=4, default=None, blank=True, null=True)
    return_on_real_estate = models.DecimalField(max_digits=8, decimal_places=4, default=None, blank=True, null=True)
    home_prices = models.DecimalField(max_digits=8, decimal_places=2, default=None, blank=True, null=True)
    cpi = models.DecimalField(max_digits=8, decimal_places=4, default=None, blank=True, null=True)
    risk_premium = models.DecimalField(max_digits=8, decimal_places=4, default=None, blank=True, null=True) # Geometric rp

    @property
    def aaa_rate(self):
        return round(100*self.aaa)/10000

    @property
    def bbb_rate(self):
        return round(100*self.bbb)/10000

    @property
    def tb3ms_rate(self):
        try:
            r = round(100*self.tb3ms)/10000
        except Exception as ex:
            r = None
        return r

    @property
    def cpi_rate(self):
        try:
            r = round(100*self.cpi)/10000
        except Exception as ex:
            r = None
        return r

    @property
    def tb3ms_rate_real(self):
        try:
            nr = 1 + self.tb3ms_rate
            ni = 1 + float(self.cpi_rate)
            rr = nr/ni - 1
        except Exception as ex:
            rr = None
            return rr
        return round(10000*rr)/10000

    @property
    def return_on_tbond(self):
        try:
            r0 = float(XBRLHistoricalReturnsSP.objects.get(year=int(self.year)-1).tb10y)
            r1 = float(self.tb10y)
            r = ((r0*(1-(1+r1)**(-10))/r1+1/(1+r1)**10)-1)+r0
        except Exception as ex:
            r = None
            return r
        return round(10000*r)/10000

        # return self.long_term_rating.default_spread

    @property
    def return_on_tbond_real(self):
        try:
            nr = 1 + self.return_on_tbond
            ni = 1 + float(self.cpi_rate)
            rr = nr/ni - 1
        except Exception as ex:
            rr = None
            return rr
        return round(10000*rr)/10000

    @property
    def dividends(self):
        try:
            d = self.sp500 * self.dividend_yield
        except Exception as ex:
            d = None
        return d

    @property
    def return_on_aaa(self):
        try:
            r0 = float(XBRLHistoricalReturnsSP.objects.get(year=int(self.year)-1).aaa_rate)
            r1 = float(self.aaa_rate)
            r = ((r0*(1-(1+r1)**(-10))/r1+1/(1+r1)**10)-1)+r0
        except Exception as ex:
            r = None
            return r
        return round(10000*r)/10000

    @property
    def return_on_bbb(self):
        try:
            r0 = float(XBRLHistoricalReturnsSP.objects.get(year=int(self.year)-1).bbb_rate)
            r1 = float(self.bbb_rate)
            r = ((r0*(1-(1+r1)**(-10))/r1+1/(1+r1)**10)-1)+r0
        except Exception as ex:
            r = None
            return r
        return round(10000*r)/10000

    @property
    def return_on_bbb_real(self):
        try:
            nr = 1 + self.return_on_bbb
            ni = 1 + float(self.cpi_rate)
            rr = nr/ni - 1
        except Exception as ex:
            rr = None
            return rr
        return round(10000*rr)/10000

    @property
    def return_on_sp500(self):
        try:
            sp0 = float(XBRLHistoricalReturnsSP.objects.get(year=int(self.year)-1).sp500)
            sp1 = float(self.sp500)
            div = float(self.dividends)
            r = (sp1-sp0+div)/sp0
        except Exception as ex:
            r = None
            return r
        return round(10000*r)/10000

    @property
    def return_on_sp500_real(self):
        try:
            nr = 1 + self.return_on_sp500
            ni = 1 + float(self.cpi_rate)
            rr = nr/ni - 1
        except Exception as ex:
            rr = None
            return rr
        return round(10000*rr)/10000

    @property
    def stock_tbill_return(self):
        try:
            r = float(self.return_on_sp500) - float(self.tb3ms_rate)
        except Exception as ex:
            r = None
            return r
        return round(10000*r)/10000

    @property
    def stock_tbonds_return(self):
        try:
            r = float(self.return_on_sp500) - float(self.return_on_tbond)
        except Exception as ex:
            r = None
            return r
        return round(10000*r)/10000

    @property
    def stock_baa_return(self):
        try:
            r = float(self.return_on_sp500) - float(self.return_on_bbb)
        except Exception as ex:
            r = None
            return r
        return round(10000*r)/10000

    def __str__(self):
        return str(self.year) + " = " + str(self.aaa)


class XBRLValuationCompanyUser(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRL Company Info')
        verbose_name_plural = _('XBRL Companies Info')
        ordering = ['company', 'user']
    #
    company = models.ForeignKey(XBRLCompanyInfo, on_delete=models.CASCADE, default=None, blank=True, null=True,
                                related_name='valuation_companies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE,
                             related_name='valuation_users')
    analysis = PlaceholderField('valuation_analysis_user')
    #

    def __str__(self):
        return self.user.name + " " + self.company


class XBRLYearsCompanyOperations(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRL Year Company Of Operations')
        verbose_name_plural = _('XBRL Year companies Of Operations')
        ordering = ['year']
    #
    company = models.ForeignKey(XBRLCompanyInfo, on_delete=models.CASCADE, default=None, blank=True, null=True,
                                related_name="years_of_operation")
    year = models.SmallIntegerField(default=2020)

    def __str__(self):
        return str(self.company.company_name) + ": " + str(self.year)


class XBRLCountriesOfOperations(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRL Country Of Operations')
        verbose_name_plural = _('XBRL Countries Of Operations')
        ordering = ['country']
    #
    company_year = models.ForeignKey(XBRLYearsCompanyOperations, on_delete=models.CASCADE, default=None, blank=True,
                                     null=True, related_name="countries_of_operation")
    country = models.ForeignKey(XBRLCountry, on_delete=models.CASCADE, default=None, blank=True, null=True,
                                related_name="company_year_countries")
    revenues = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rating = models.CharField(max_length=10, default='')
    spread = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    risk_premium = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


class XBRLRegionsOfOperations(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRL region Of Operations')
        verbose_name_plural = _('XBRL regions Of Operations')
        ordering = ['region']
    #
    company_year = models.ForeignKey(XBRLYearsCompanyOperations, on_delete=models.CASCADE, default=None, blank=True,
                                     null=True, related_name="regions_of_operation")
    region = models.ForeignKey(XBRLRegion, on_delete=models.CASCADE, default=None, blank=True, null=True,
                               related_name="company_year_regions")
    revenues = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rating = models.CharField(max_length=10, default='')
    spread = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    risk_premium = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


class XBRLIndustryBetasOfOperations(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRL industry beta Of Operations')
        verbose_name_plural = _('XBRL industry betas Of Operations')
        ordering = ['industry']
    #
    company_year = models.ForeignKey(XBRLYearsCompanyOperations, on_delete=models.CASCADE, default=None, blank=True,
                                     null=True, related_name="industries_of_operation")
    industry = models.ForeignKey(GlobalIndustryAverages, on_delete=models.CASCADE, default=None, blank=True, null=True,
                                 related_name="company_year_industries")
    revenues = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ev_over_sales = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estimated_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unlevered_beta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estimated_growth = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


class XBRLCountryYearData(TruncateTableMixin, models.Model):
    project = None

    class Meta:
        verbose_name = _('XBRL Country Year Data')
        verbose_name_plural = _('XBRL Countries Year Data')
        ordering = ['country', 'year']

    # The following are dimensions
    country = models.ForeignKey(XBRLCountry, on_delete=models.CASCADE, default=None, blank=True, null=True,
                                related_name='country_data')
    year = models.PositiveSmallIntegerField(default=0)
    # The followings are measures
    tax_rate = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    gdp = models.DecimalField(max_digits=12, decimal_places=5, blank=True, null=True)
    sp_rating = models.CharField(max_length=250, default='')
    moodys_rating = models.CharField(max_length=20, default='')
    composite_risk_rating = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    cds = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    # Managers
    objects = models.Manager()  # The default manager.
    project_objects = XBRLCountryYearDataProject()  # The project manager.

    # Properties
    @property
    def moodys_rate_completed_by_sp(self):
        # print(self.country)
        if str(self.moodys_rating) == '':
            try:
                sp_ = XBRLSPMoodys.objects.get(year=self.year, sp=self.sp_rating).sp
            except Exception as ex:
                # print(self.sp_rating)
                # print(self.year)
                # print(ex)
                sp_ = 'kk'
            # print(sp_)
        else:
            sp_ = str(self.moodys_rating)
        return sp_

    # rating
    @property
    def rating_based_default_spread(self):
        # print(self.country)
        try:
            ds_ = XBRLSPMoodys.objects.get(year=self.year, moodys=self.moodys_rate_completed_by_sp).default_spread
        except Exception as ex1:
            # print('error 100 ' + str(ex1))
            try:
                # print(self.country)
                # print(self.composite_risk_rating)

                ds_ = XBRLSPMoodys.objects.filter(year=self.year, score_from__lte=self.composite_risk_rating,
                                                  score_to__gte=self.composite_risk_rating).all()[0]
                # print('ds_1111')
                # print(ds_)
                ds_ = ds_.default_spread
                # print('ds_2222')
                # print(ds_)

            except Exception as ex:
                # print('error200 ' + str(ex))
                ds_ = None
        return ds_

    @property
    def country_risk_premium_rating(self):
        if self.project:
            try:
                ds_ = round(100*float(self.rating_based_default_spread) * float(self.project.volatility_ratio))/100
            except Exception as ex:
                ds_ = 0
        else:
            ds_ = None
        return ds_

    @property
    def total_equity_risk_premium_rating(self):
        try:
            if self.project:
                try:
                    ds_ = round(100*float(self.country_risk_premium_rating) + float(self.project.mature_marker_risk_premium))/100
                except Exception as ex:
                    ds_ = 0
            else:
                ds_ = None
            return ds_
        except Exception as ex:
            ds = None
        return ds

    # cds
    @property
    def excess_cds_spread_over_us_cds(self):
        try:
            country = XBRLCountry.objects.get(name='United States')
            us_cds = XBRLCountryYearData.objects.get(country=country, year=self.year).cds
            this_cds = XBRLCountryYearData.objects.get(country=self.country, year=self.year).cds
            d = this_cds - us_cds
            if d <= 0:
                d = 0
        except Exception as ex:
            d = None
        return d

    @property
    def country_risk_cds(self):
        try:
            if self.project:
                try:
                    ds_ = round(100*float(self.excess_cds_spread_over_us_cds) * float(self.project.volatility_ratio))/100
                except Exception as ex:
                    ds_ = 0
            else:
                ds_ = None
            return ds_
        except Exception as ex:
            ds = None
        return ds

    @property
    def total_equity_risk_premium_cds(self):
        try:
            if self.project:
                try:
                    ds_ = round(100*float(self.country_risk_cds) + float(self.project.mature_marker_risk_premium))/100
                except Exception as ex:
                    ds_ = 0
            else:
                ds_ = None
            return ds_
        except Exception as ex:
            ds = None
        return ds

    def __str__(self):
        return str(self.country)
        # + " : " + str(self.year) + " : " + str(self.tax_rate)


#
# # https://www.moodys.com/researchandratings/market-segment/sovereign-supranational/-/005005?tb=2&sbk=issr_name&sbo=1
# class XBRLCountryPremium(TruncateTableMixin, models.Model):
#     class Meta:
#         verbose_name = _('XBRLCountryPremium')
#         verbose_name_plural = _('XBRLCountryPremium')
#         ordering = ['company', 'account']
#
#     country = models.ForeignKey(XBRLCountry, on_delete=models.CASCADE, default=None, blank=True, null=True)
#
    # parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', default=1)


# Options
class XBRLSPStatistics(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRLSPStatistic')
        verbose_name_plural = _('XBRLSPStatistics')
        ordering = ['next_release_date']
    #
    company = models.OneToOneField(XBRLCompanyInfo, on_delete=models.CASCADE, default=None,
                                   related_name='company_statistic')
    next_release_date = models.DateField(blank=True, null=True)
    mean_abs_price_change = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    mean_abs_actual_forecast_change = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    mean_abs_actual_forecast_change_money = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    correlation_afp = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    updated = models.DateField(blank=True, null=True)
    straddle_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    butterfly_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    announcement_time = models.CharField(max_length=1, default='', blank=True, null=True)

    def set_company_statistics(self, is_update=True):
        # print('---111--- set_company_statistics ------')
        log_debug("Start set_company_statistics for: " + self.company.ticker)
        # print(self.company.ticker)
        tmp = []
        tafc = []
        taf = []
        efs = XBRLSPEarningForecast.objects.filter(company=self.company).order_by('-year', '-quarter').all()[:5]
        for e in efs:
            try:
                if e.forecast == 0 or e.yesterday_price == 0:
                    continue
                pa = abs(e.today_price - e.yesterday_price)  # / e.yesterday_price)
                afc = abs((e.actual - e.forecast))
                af = abs(afc / e.forecast)

                tmp.append(pa)
                tafc.append(afc)
                taf.append(af)
            except Exception as ex:
                pass
        try:

            mp = sum(tmp)/len(tmp)
            mp = round(100 * mp)/100
            # if self.company.ticker == "PYPL":
            #     print(len(tmp))
            #     print(tmp)
            #     print(mp)
            self.mean_abs_price_change = mp

            maf = sum(taf)/len(taf)
            mafc = sum(tafc)/len(tafc)
            maf = round(10000 * maf)/100
            self.mean_abs_actual_forecast_change = maf
            self.mean_abs_actual_forecast_change_money = mafc

            tmp = [float(x) for x in tmp]
            taf = [float(x) for x in taf]

            if len(tmp) > 1:
                corr, p_value = pearsonr(tmp, taf)
                corr = round(100*corr)/100
                self.correlation_afp = corr
            if is_update:
                d = (datetime.datetime.now() + timedelta(hours=-7)).date()
                self.updated = d
            self.save()
        except Exception as ex:
            # print("error 201 save mp: " + str(ex))
            log_debug("Error 201 save mp for: " + self.company.ticker)
        # print("End set_company_statistics: " + self.company.ticker)
        # log_debug("End set_company_statistics: " + self.company.ticker)


class XBRLSPStrategies(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRLSPStrategy')
        verbose_name_plural = _('XBRLSPStrategies')
        ordering = ['company']
    #
    created = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(XBRLCompanyInfo, on_delete=models.CASCADE, default=None,
                                related_name='company_strategies')
    previous_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    condor_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    call_delta_low = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    call_strike_low = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    call_price_low = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    call_delta_high = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    call_strike_high = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    call_price_high = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    put_delta_low = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    put_strike_low = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    put_price_low = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    put_delta_high = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    put_strike_high = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    put_price_high = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)


class XBRLSPEarningForecast(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRLSPEarningForcast')
        verbose_name_plural = _('XBRLSPEarningForcast')
        ordering = ['next_release_date']
    #
    created = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(XBRLCompanyInfo, on_delete=models.CASCADE, default=None,
                                related_name='company_forecast')
    forecast = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    actual = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    next_release_date = models.DateField(blank=True, null=True)
    year = models.PositiveSmallIntegerField(default=datetime.datetime.now().year, blank=True)
    quarter = models.PositiveSmallIntegerField(default=math.ceil(datetime.datetime.now().month / 3), blank=True)
    today_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    yesterday_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


# Trading data daily and archive ---
# we have a function to move daily data to archive --
class XBRLRealEquityPrices(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRLRealEquityPrices')
        verbose_name_plural = _('XBRLRealEquityPrices')
        ordering = ['ticker']
    #
    ticker = models.CharField(max_length=10, null=False)
    t = models.PositiveBigIntegerField(default=0)
    o = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    h = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    l = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    c = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    v = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.ticker


class XBRLRealEquityPricesArchive(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRLRealEquityPricesArchive')
        verbose_name_plural = _('XBRLRealEquityPricesArchive')
        ordering = ['ticker']
    #
    ticker = models.CharField(max_length=10, null=False)
    t = models.PositiveBigIntegerField(default=0)
    o = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    h = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    l = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    c = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    v = models.PositiveBigIntegerField(default=0)


# XBRL data collection -- Accounting --
class XBRLValuationStatementsAccounts(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRLValuationStatementsAccount')
        verbose_name_plural = _('XBRLValuationStatementsAccounts')
        ordering = ['order']
    #
    order = models.PositiveSmallIntegerField(default=0)
    statement = models.CharField(max_length=250, default='Income Statement')

    def __str__(self):
        return str(self.statement)


class XBRLValuationAccounts(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRLValuationAccount')
        verbose_name_plural = _('XBRLValuationAccounts')
        ordering = ['order']
    #
    sic = models.PositiveSmallIntegerField(default=0)
    order = models.PositiveSmallIntegerField(default=0)
    account = models.CharField(max_length=250, null=True)
    type = models.SmallIntegerField(default=1)   # 1 balance sheet 2 income statement -1 all
    statement = models.ForeignKey(XBRLValuationStatementsAccounts, on_delete=models.CASCADE, default=None, blank=True,
                                  null=True, related_name='xbrl_valuation_statements')
    scale = models.PositiveIntegerField(default=1000000)

    def __str__(self):
        return self.account


class XBRLValuationAccountsMatch(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRLValuationAccountMatch')
        verbose_name_plural = _('XBRLValuationAccountsMatch')
        ordering = ['company']
    #
    year = models.PositiveSmallIntegerField(default=0)
    company = models.ForeignKey(XBRLCompanyInfo, on_delete=models.CASCADE, default=None, blank=True, null=True,
                                related_name='xbrl_valuation_accounts_match')
    account = models.ForeignKey(XBRLValuationAccounts, on_delete=models.CASCADE, default=None, blank=True, null=True)
    match_account = models.CharField(max_length=250, null=True)
    accounting_standard = models.CharField(max_length=250, default="us-gaap")


# -- Business Intelligence --
# -- The Accounting Cube --
class XBRLDimCompany(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRL Dim Company')
        verbose_name_plural = _('XBRL Dim Companies')
        ordering = ['main_sic_code', 'sic_code', 'company_name']
    #
    id = models.PositiveSmallIntegerField(primary_key=True)
    main_sic_code = models.PositiveSmallIntegerField()
    main_sic_description = models.CharField(max_length=128, default='', blank=True, null=True)
    sic_code = models.PositiveSmallIntegerField()
    sic_description = models.CharField(max_length=128, default='', blank=True, null=True)
    exchange = models.CharField(max_length=10, default='nyse')

    ticker = models.CharField(max_length=10, null=False)
    cik = models.CharField(max_length=10, null=True)
    company_name = models.CharField(max_length=128, default='', blank=True, null=True)
    city = models.CharField(max_length=50, default="", blank=True)
    state = models.CharField(max_length=50, default="", blank=True)
    zip = models.CharField(max_length=10, default="", blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.ticker) + ":" + str(self.company_name)


class XBRLDimTime(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRL Dim Time')
        verbose_name_plural = _('XBRL Dim Time')
        ordering = ['year', 'quarter']
    #
    id = models.PositiveSmallIntegerField(primary_key=True)
    year = models.PositiveSmallIntegerField(default=0)
    quarter = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.id)


class XBRLDimAccount(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRL Dim Account')
        verbose_name_plural = _('XBRL Dim Account')
        ordering = ['statement_order', 'order']
    #
    order = models.PositiveSmallIntegerField(default=0, primary_key=True)
    statement_order = models.PositiveSmallIntegerField(default=0)
    statement = models.CharField(max_length=250, default='Income Statement')
    account = models.CharField(max_length=250, null=True)
    parent = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.order) + ":" + str(self.account)


class XBRLFactCompany(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRL Fact Company')
        verbose_name_plural = _('XBRL Fact Companies')

    company = models.ForeignKey(XBRLDimCompany, on_delete=models.CASCADE, default=None, related_name='dim_companies')
    time = models.ForeignKey(XBRLDimTime, on_delete=models.CASCADE, default=None, related_name='dim_times')
    account = models.ForeignKey(XBRLDimAccount, on_delete=models.CASCADE, default=None, related_name='dim_companies')
    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)

# needs a matching matrix to calculate special accounts (by industry)
# so that account will include the ones in the XBRLDimAccount and the special calculated ones
# which will be used in XBRLRatioDim
# (3) complete accounts             NEED TO BE DONE
# () create special accounts        DONE
# () fill XBRLFactRatiosCompany     DONE
#     For every ration in XBRLRatioDim, calculate the ration and put it in XBRLFactRatiosCompany
class XBRLProcessedFactCompany(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRL Processed Fact Company')
        verbose_name_plural = _('XBRL Processed Fact Companies')

    company = models.ForeignKey(XBRLDimCompany, on_delete=models.CASCADE, default=None, related_name='dim_processed_companies')
    time = models.ForeignKey(XBRLDimTime, on_delete=models.CASCADE, default=None, related_name='dim_processed_times')
    account = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    def __str__(self):
        return str(self.company) + ":" + str(self.amount)

# in the adjectives we have accounts_group
class XBRLAccountsGroupsFactCompany(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRL Accounts Groups Fact Company')
        verbose_name_plural = _('XBRL Accounts Groups Fact Companies')

    company = models.ForeignKey(XBRLDimCompany, on_delete=models.CASCADE, default=None, related_name='dim_accounts_groups_companies')
    time = models.ForeignKey(XBRLDimTime, on_delete=models.CASCADE, default=None, related_name='dim_accounts_groups_times')
    account = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)

class XBRLRatioDim(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRL Ratio Dim')
        verbose_name_plural = _('XBRL Ratio Dims')
        ordering = ['industry', 'ratio_group']
    #
    industry = models.PositiveSmallIntegerField(default=0)
    ratio_group = models.PositiveSmallIntegerField(default=0)
    ratio_name = models.CharField(max_length=250, null=True)
    numerator = models.IntegerField(default=0)
    denominator = models.IntegerField(default=0)

    def __str__(self):
        return str(self.industry) + ":" + str(self.ratio_group) + ":"  + str(self.ratio_name)

class XBRLFactRatiosCompany(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('XBRL Fact Ratios Company')
        verbose_name_plural = _('XBRL Fact Ratios Companies')

    company = models.ForeignKey(XBRLDimCompany, on_delete=models.CASCADE, default=None, related_name='dim_ratio_companies')
    time = models.ForeignKey(XBRLDimTime, on_delete=models.CASCADE, default=None, related_name='dim_ratio_times')
    ratio = models.ForeignKey(XBRLRatioDim, on_delete=models.CASCADE, default=None, related_name='dim_ratio_ratio')
    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    def __str__(self):
        return str(self.company) + ":" + str(self.ratio) + ":"  + str(self.amount)

# -- Admin tables --
class ToDoList(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('todolist')
        verbose_name_plural = _('todolist')
        ordering = ['-is_active', '-priority', 'description']

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE,
                             related_name='user_to_do_lists')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    subject = models.CharField(max_length=150, null=False)
    description = models.CharField(max_length=1000, null=False)
    priority = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.subject

#
class CorporateValuationWeb(TruncateTableMixin, models.Model):
    company_name = models.CharField(max_length=100, default='', blank=True, null=True)
    address = models.CharField(max_length=50, default='', blank=True, null=True)

    def __str__(self):
        return self.company_name

#
class Adjectives(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return str(self.title)


class AdjectiveQuerySet(models.QuerySet):
    def adjectives(self, adjective_title):
        return self.filter(adjective__title=adjective_title)


class AdjectiveManager(models.Manager):
    def get_queryset(self):
        return AdjectiveQuerySet(self.model, self._db)

    def adjectives(self, adjective_title):
        return self.get_queryset().adjectives(adjective_title).order_by("order")


class AdjectivesValues(models.Model):
    adjective = models.ForeignKey(Adjectives, on_delete=models.CASCADE)
    order = models.SmallIntegerField(blank=True, default=1)
    value = models.CharField(max_length=50)

    objects = models.Manager()  # The default manager.
    adjectives = AdjectiveManager()  # Our custom manager.

    def __str__(self):
        return self.value


# StockPrices
class StockPricesMinutes(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('StockPricesMinute')
        verbose_name_plural = _('StockPricesMinutes')
        ordering = ['company__id', '-idx']

    company = models.ForeignKey(XBRLCompanyInfo, on_delete=models.CASCADE, default=None, blank=True, null=True,
                                related_name='company_info_stock_prices')
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


class StockPricesDays(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('StockPricesDay')
        verbose_name_plural = _('StockPricesDays')
        ordering = ['company__id', '-idx']

    company = models.ForeignKey(XBRLCompanyInfo, on_delete=models.CASCADE, default=None, blank=True, null=True,
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


class TwoSpreadStrategy(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('TwoSpreadStrategy')
        verbose_name_plural = _('TwoSpreadStrategys')
        ordering = ['strategy_idx']

    company = models.ForeignKey(XBRLCompanyInfo, on_delete=models.CASCADE, default=None, blank=True, null=True,
                                related_name='two_spread_strategys')
    strategy_idx = models.PositiveBigIntegerField(default=0)
    strike = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return str(self.strategy_idx) + ": " + str(self.strike)

class TwoSpreadStrategyDetails(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = _('TwoSpreadStrategyDetail')
        verbose_name_plural = _('TwoSpreadStrategyDetails')
        ordering = ['stock_price']

    two_spread_strategy = models.ForeignKey(TwoSpreadStrategy, on_delete=models.CASCADE, default=None, blank=True,
                                            null=True, related_name='two_spread_strategy_details')
    idx = models.PositiveBigIntegerField(default=0)
    seconds = models.PositiveBigIntegerField(default=0)
    stock_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    strategy_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return str(self.idx)