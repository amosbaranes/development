from __future__ import unicode_literals
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
import datetime
from django.db import models
# from django.utils.encoding import python_2_unicode_compatible, force_text
from django.utils.translation import ugettext_lazy as _, get_language

from filer.fields.image import FilerImageField
from cms.models.fields import PlaceholderField

# from parler.models import TranslatableModel, TranslatedFields
from parler.models import TranslatableModel, TranslatableModelMixin, TranslatedFields, TranslatableManager


from django.core.validators import MinValueValidator, MaxValueValidator
from parler.utils.context import switch_language
from django.shortcuts import get_object_or_404
import numpy as np
import pandas as pd
from django.utils.text import slugify
from ..core.fields import OrderField
from ..courses.models import (CourseSchedule, CourseScheduleUser, Team)
from django.db.models import Avg, Sum, Min, Max


def boltzman(x, xmid, tau):
    return 1. / (1. + np.exp(-(x-xmid)/tau))


class ModelGlobalSim(models.Model):

    class Meta:
        abstract = True
        ordering = ['order']

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    description = PlaceholderField('game_type_description')
    image = FilerImageField(blank=True, null=True, on_delete=models.SET_NULL)
    order = models.PositiveSmallIntegerField(default=1)


class TranslatableModelGlobalSim(TranslatableModelMixin, ModelGlobalSim):
    """
    Base model class to handle translations.
    All translatable fields will appear on this model, proxying the calls to the :class:`TranslatedFieldsModel`.
    I duplicated the TranslatableModel structure and added basic fields.
    """
    class Meta:
        abstract = True

    # change the default manager to the translation manager
    objects = TranslatableManager()


class GameType(TranslatableModelGlobalSim):

    class Meta:
        verbose_name = _('game type')
        verbose_name_plural = _('game types')

    #
    translations = TranslatedFields(
        name=models.CharField(_('name'), blank=False, default='', help_text=_('Please supply the game type.'),
                              max_length=128),
        slug=models.SlugField(_('slug'), blank=True, default='', help_text=_('Please supply the game type slug.'),
                              max_length=128)
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.id) + '-' + self.name + '-' + get_language())
        super(GameType, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class Segment(TranslatableModelGlobalSim):

    class Meta:
        verbose_name = _('segment')
        verbose_name_plural = _('segments')
    #
    game_type = models.ForeignKey(GameType, on_delete=models.CASCADE, null=True, related_name='segments')
    #
    translations = TranslatedFields(
        name=models.CharField(_('name'), blank=False, default='', help_text=_('Please supply the segment name.'),
                              max_length=128),
        slug=models.SlugField(_('slug'), blank=True, default='', help_text=_('Please supply the segment slug.'),
                              max_length=128)
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.id) + '-' + self.name + '-' + get_language())
        super(Segment, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class Attribute(TranslatableModelGlobalSim):

    class Meta:
        verbose_name = _('attribute')
        verbose_name_plural = _('attributes')

    segment = models.ForeignKey(Segment, on_delete=models.CASCADE, related_name='attributes')
    #
    start_optimal_value = models.SmallIntegerField(default=1)
    tau_improvments = models.SmallIntegerField(default=5)
    tau_miss_match = models.SmallIntegerField(default=5)

    #
    def get_period_optimal_value(self, period_number):
        ag = np.round(boltzman(period_number, 0, self.tau_improvments) - 0.5, 2)
        return self.start_optimal_value * (1+ag)
    #
    translations = TranslatedFields(
        name=models.CharField(_('name'), blank=False, default='', help_text=_('Please supply the section name.'),
                              max_length=128),
        slug=models.SlugField(_('slug'), blank=True, default='', help_text=_('Please supply the section slug.'),
                              max_length=128)
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.id) + '-' + self.segment.name + '-' + self.name + '-' + get_language())
        super(Attribute, self).save(*args, **kwargs)

    def __str__(self):
        return self.segment.name + '-' + self.name


class ProductTypeAttribute(TranslatableModelGlobalSim):

    TYPE = (
        (10, _('Advertising'), _('TV')),
        (20, _('Advertising'), _('internet')),
        (30, _('Advertising'), _('magazine')),
        (110, _('PublicRelation'), _('TV')),
        (120, _('PublicRelation'), _('internet')),
        (130, _('PublicRelation'), _('magazine')),
        (204, _('Product'), _('retail_price')),
        (208, _('Product'), _('planned_production')),
        (212, _('Product'), _('inventory_finished_goods')),
        (216, _('Product'), _('inventory_raw_material')),
        (220, _('Product'), _('quality_system')),
        (224, _('Product'), _('quality_inspection')),
        (230, _('Product'), _('randd'))
    )

    class Meta:

        verbose_name = _('product_type_attribute')
        verbose_name_plural = _('product_type_attributes')
    #
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE, null=True,
                                default=None, related_name='product_attributes')

    category = models.CharField(_('category'), blank=False, default='',
                                help_text=_('Please supply category.'), max_length=128)
    account = models.CharField(_('account'), blank=False, default='',
                               help_text=_('Please supply account.'), max_length=128)
    account_number = models.IntegerField(default=0, null=True)
    #
    amount = models.IntegerField(default=0)
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=200)
    #
    translations = TranslatedFields(
        name=models.CharField(_('name'), blank=False, default='', help_text=_('Please supply product attribute type.'),
                              max_length=128),
        slug=models.SlugField(_('slug'), blank=True, default='', help_text=_('Please supply product attribute slug.'),
                              max_length=128)
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.id) + '-' + self.name + '-' + get_language())
        super(ProductTypeAttribute, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ManufacturingTypeAttribute(TranslatableModelGlobalSim):

    TYPE = (
        (10, _('Process'), _('technology_improvement')),
        (20, _('Process'), _('supply_chain_management_system')),
        (30, _('Process'), _('warehousing')),
        (110, _('Plant'), _('size')),
        (210, _('Quality'), _('internal_control')),
    )

    class Meta:
        verbose_name = _('manufacturing_type_attribute')
        verbose_name_plural = _('manufacturing_type_attributes')

    game_type = models.ForeignKey(GameType, on_delete=models.CASCADE, null=True,
                                  default=None, related_name='manufacturing_attributes')

    category = models.CharField(_('category'), blank=False, default='',
                                help_text=_('Please supply category.'), max_length=128)
    account = models.CharField(_('account'), blank=False, default='',
                               help_text=_('Please supply account.'), max_length=128)
    account_number = models.IntegerField(default=0, null=True)
    #
    amount = models.IntegerField(default=0)
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=200)
    #
    translations = TranslatedFields(
        name=models.CharField(_('name'), blank=False, default='', help_text=_('Please supply manuf. attribute type.'),
                              max_length=128),
        slug=models.SlugField(_('slug'), blank=True, default='', help_text=_('Please supply manuf. attribute slug.'),
                              max_length=128)
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.id) + '-' + self.name + '-' + get_language())
        super(ManufacturingTypeAttribute, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class HumanResourcesTypeAttribute(TranslatableModelGlobalSim):

    TYPE = (
        (10, _('Salary'), _('employee_salary')),
        (20, _('Salary'), _('manager_salary')),
        (30, _('Salary'), _('number_of_managers')),
        (40, _('Salary'), _('number_of_employees')),
        (50, _('Salary'), _('benefits')),
        (110, _('Quality'), _('employee_training')),
        (120, _('Quality'), _('manager_training')),
    )

    class Meta:
        verbose_name = _('human_resources_type_attribute')
        verbose_name_plural = _('human_resources_type_attributes')

    game_type = models.ForeignKey(GameType, on_delete=models.CASCADE, null=True,
                                  default=None, related_name='human_resources_attributes')
    category = models.CharField(_('category'), blank=False, default='',
                                help_text=_('Please supply category.'), max_length=128)
    account = models.CharField(_('account'), blank=False, default='',
                               help_text=_('Please supply account.'), max_length=128)
    account_number = models.IntegerField(default=0, null=True)
    #
    amount = models.IntegerField(default=0)
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=200)
    #
    translations = TranslatedFields(
        name=models.CharField(_('name'), blank=False, default='', help_text=_('Please supply product attribute type.'),
                              max_length=128),
        slug=models.SlugField(_('slug'), blank=True, default='', help_text=_('Please supply product attribute slug.'),
                              max_length=128)
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.id) + '-' + self.name + '-' + get_language())
        super(HumanResourcesTypeAttribute, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Distributor(TranslatableModelGlobalSim):

    class Meta:
        verbose_name = _('distributor')
        verbose_name_plural = _('distributors')

    game_type = models.ForeignKey(GameType, on_delete=models.CASCADE, null=True, related_name='distributors')

    number_of_location = models.PositiveIntegerField(default=200)
    logistic_support = models.PositiveIntegerField(default=200)

    translations = TranslatedFields(
        name=models.CharField(_('name'), blank=False, default='', help_text=_('Please supply the distributor name.'),
                              max_length=128),
        slug=models.SlugField(_('slug'), blank=True, default='', help_text=_('Please supply the distributor slug.'),
                              max_length=128)
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.id) + '-' + self.name + '-' + get_language())
        super(Distributor, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class DistributorAttribute(TranslatableModelGlobalSim):

    class Meta:
        verbose_name = _('distributor_attribute')
        verbose_name_plural = _('distributor_attributes')

    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE, related_name='distributor_attributes')
    #
    amount = models.IntegerField(default=0)
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=200)
    #
    translations = TranslatedFields(
        name=models.CharField(_('name'), blank=False, default='', help_text=_('Please supply the section name.'),
                              max_length=128),
        slug=models.SlugField(_('slug'), blank=True, default='', help_text=_('Please supply the section slug.'),
                              max_length=128)
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.id) + '-' + self.name + '-' + get_language())
        super(DistributorAttribute, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class DistributorSegment(models.Model):
    class Meta:
        verbose_name = _('distributor_segment')
        verbose_name_plural = _('distributor_segments')

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE, null=True,
                                    related_name='distributor_segments')

    segment = models.ForeignKey(Segment, on_delete=models.CASCADE, null=True, related_name='segment_distributors')
    percentage = models.IntegerField(default=50)

    def __str__(self):
        return self.distributor.name + "-" + self.segment.name


class FinanceType(TranslatableModelGlobalSim):
    class Meta:
        verbose_name = _('finance_type')
        verbose_name_plural = _('finance_types')
        ordering = ['order']

    game_type = models.ForeignKey(GameType, on_delete=models.CASCADE, null=True,
                                  related_name='finance_types')

    translations = TranslatedFields(
        name=models.CharField(_('name'), blank=False, default='', help_text=_('Please supply the finance type name.'),
                              max_length=128),
        slug=models.SlugField(_('slug'), blank=True, default='', help_text=_('Please supply the finance type slug.'),
                              max_length=128)
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.id) + '-' + self.name + '-' + get_language())
        super(FinanceType, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# @python_2_unicode_compatible
class FinanceTypeAttribute(TranslatableModelGlobalSim):
    class Meta:
        verbose_name = _('finance_type_attribute')
        verbose_name_plural = _('finance_type_attributes')
        ordering = ['order']

    finance_type = models.ForeignKey(FinanceType, on_delete=models.CASCADE, related_name='finance_attributes')
    #
    amount = models.IntegerField(default=0)
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=200)
    #
    translations = TranslatedFields(
        name=models.CharField(_('name'), blank=False, default='', help_text=_('Please supply the section name.'),
                              max_length=128),
        slug=models.SlugField(_('slug'), blank=True, default='', help_text=_('Please supply the section slug.'),
                              max_length=128)
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.id) + '-' + self.name + '-' + get_language())
        super(FinanceTypeAttribute, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# ===================================================================
class Game(TranslatableModelGlobalSim):
    STATUS = (
        (0, 'Created'),
        (5, 'Approved'),
        (10, 'Student Registration'),
        (20, 'End Registration'),
        (30, 'Running'),
        (100, 'Finished')
    )
    PERIOD_TYPE = (
        (0, 'Year'),
        (5, 'Period')
    )

    class Meta:
        verbose_name = _('game')
        verbose_name_plural = _('games')

    #
    game_type = models.ForeignKey(GameType, on_delete=models.CASCADE, null=True, related_name='games')
    course_schedule = models.OneToOneField(CourseSchedule, on_delete=models.CASCADE, null=True, related_name='game')
    #
    status = models.IntegerField(default=0, choices=STATUS)
    number_of_periods = models.IntegerField(default=8)
    current_period_number = models.PositiveIntegerField(default=1)
    period_type = models.IntegerField(default=0, choices=PERIOD_TYPE)

    # relative to starting period 0 or a specific yea
    # can extend to months or quarters
    @property
    def start_period(self):
        if self.period_type == 0:
            return self.created.year
        elif self.period_type == 5:
            return 0

    def get_current_team(self, user):
        course_schedule_ = self.course_schedule
        # teams = course_schedule_.schedule_teams.all()
        csu = get_object_or_404(CourseScheduleUser, course_schedule=course_schedule_, user=user)
        team_ = csu.team
        return team_

    @property
    def teams(self):
        return self.course_schedule.schedule_teams.all()

    @property
    def current_period(self):
        return self.start_period + self.current_period_number

    @property
    def current_period_obj(self):
        try:
            current_period_obj_ = self.game_periods.filter(period_number=self.current_period_number)[0]
        except Exception as e:
            # print("Models-100 :" + e)
            current_period_obj_ = self.create_period(n_period=self.current_period_number)
        return current_period_obj_

    @property
    def next_period_obj(self):
        try:
            next_period_obj_ = self.game_periods.filter(period_number=self.current_period_number+1)[0]
        except Exception as e:
            # print(e)
            next_period_obj_ = self.create_next_period()
        return next_period_obj_

    def create_next_period(self):
        # enter date in this way: '17/07/2018'
        n_ = self.current_period_number+1
        period_ = self.create_period(n_period=n_)
        return period_

    def create_period(self, n_period=0):
        # enter date in this way: '17/07/2018'
        name_ = 'period ' + str(n_period)
        period_ = Period.objects.create(game=self, period_number=n_period)
        return period_

    # Management ----
    def set_zero(self, user):
        self.game_periods.all().delete()
        self.current_period_number = 0
        self.save()
        period0 = Period.objects.create(game=self, period_number=0)
        period1 = Period.objects.create(game=self, period_number=1)
        for team_ in self.teams:
            s0 = self.game_type.segments.all()[0]
            # ToDo_
            # set default: scu_per_unit=1, prime_cost_per_unit=50, project_expenditure
            # value=a.start_optimal_value - 2
            #
            rd_ = RandD.objects.create(period=period0, team=team_, segment=s0,
                                       scu_per_unit=1,
                                       prime_cost_per_unit=50,
                                       project_expenditure=1000000,
                                       last_entered_by=user,
                                       name="RD-" + s0.name
                                       )
            for a in s0.attributes.all():
                RandD_Attribute.objects.create(
                    randd=rd_, attribute=a, value=a.start_optimal_value - 2
                )
            pr_ = rd_.get_or_create_product()
            pr_.create_detail()
            GDistributor.objects.filter(team=team_).all().delete()
            for d in self.game_type.distributors.all():
                ds = GDistributor.objects.create(team=team_, distributor=d)
                ds.create_detail()

            Finance.objects.filter(team=team_).all().delete()
            for f in self.game_type.finance_types.all():
                fs = Finance.objects.create(team=team_, finance_type=f)
                fs.create_detail()

        self.current_period_number = 1
        self.save()
        for team_ in self.teams:
            for pr_ in team_.team_products.all():
                pr_.create_detail()
            for ds_ in team_.team_g_distributors.all():
                ds_.create_detail()
            for fs_ in team_.team_finances.all():
                fs_.create_detail()

            # print("create rd for1 manufacturing: " + team_.name)
            manufacturing0 = ManufacturingPeriodData.objects.create(team=team_, period=period0)
            manufacturing1 = ManufacturingPeriodData.objects.create(team=team_, period=period1)
            # print("create rd for1 manufacturing: " + team_.name)
            manufacturing0.create_detail()
            manufacturing1.create_detail()

            human_resources0 = HumanResourcesPeriodData.objects.create(team=team_, period=period0)
            human_resources1 = HumanResourcesPeriodData.objects.create(team=team_, period=period1)
            # print("create rd for1 manufacturing: " + team_.name)
            human_resources0.create_detail()
            human_resources1.create_detail()

    def rollover(self, user):
        # Market Clearing

        # Next Period
        next_period = self.next_period_obj
        for t in self.course_schedule.schedule_teams.all():
            for p in t.team_products.all():
                if not p.abundant_period:
                    p.duplicate_detail()
            for d in t.team_g_distributors.all():
                d.duplicate_detail()
            for f in t.team_finances.all():
                f.duplicate_detail()
            t.team_manufacturing.get(period=self.current_period_obj).duplicate_detail()
            t.team_human_resources.get(period=self.current_period_obj).duplicate_detail()
        self.current_period_number += 1
        self.save()

    @property
    def get_schedule_period_dates(self):
        n_1 = int(SchedulePeriodDate.objects.count())
        n_ = int(self.number_of_periods)
        if n_ > n_1:
            for i in range(1, n_+1):
                try:
                    gspd = self.game_schedule_period_dates.get(period_number=i)
                except Exception as e:
                    gspd = SchedulePeriodDate.objects.create(game=self, period_number=i)
        elif n_ < n_1:
            print(range(n_, n_1))
            for j in range(n_+1, n_1+1):
                try:
                    self.game_schedule_period_dates.get(period_number=j).delete()
                except Exception as e:
                    pass
        return self.game_schedule_period_dates.all()

    @property
    def get_edit_game_info(self):
        for s in self.game_type.segments.all():
            for k in ProductTypeAttribute.TYPE:
                if not ProductTypeAttribute.objects.filter(account_number=k[0]).filter(segment=s).exists():
                    name_ = str(k[1])+"_"+str(k[2])
                    ProductTypeAttribute.objects.create(segment=s, account_number=k[0], category=str(k[1]),
                                                        account=str(k[2]), name=name_)

        for k in ManufacturingTypeAttribute.TYPE:
            if not ManufacturingTypeAttribute.objects.filter(account_number=k[0]).filter(game_type=self.game_type).exists():
                name_ = str(k[1]) + "_" + str(k[2])
                ManufacturingTypeAttribute.objects.create(game_type=self.game_type, account_number=k[0],
                                                          category=str(k[1]), account=str(k[2]), name=name_)

        for k in HumanResourcesTypeAttribute.TYPE:
            if not HumanResourcesTypeAttribute.objects.filter(account_number=k[0]).filter(game_type=self.game_type).exists():
                name_ = str(k[1]) + "_" + str(k[2])
                HumanResourcesTypeAttribute.objects.create(game_type=self.game_type, account_number=k[0], category=str(k[1]),
                                                           account=str(k[2]), name=name_)
        return 1

    #
    translations = TranslatedFields(
        name=models.CharField(_('name'), blank=False, default='',
                              help_text=_('Please supply the game name.'), max_length=128),
        slug=models.SlugField(_('slug'), blank=True, default='',
                              help_text=_('Please supply the game slug.'), max_length=128)
    )

    # def get_absolute_url(self):
    #     with switch_language(self, get_language()):
    #         return reverse('globsim:game_detail', kwargs={'slug': self.slug, })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.id) + '-' + self.course_schedule.name + '-' + self.name + ' ' + get_language())
        super(Game, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class SchedulePeriodDate(models.Model):
    class Meta:
        verbose_name = _('schedule_period_date')
        verbose_name_plural = _('schedule_period_date')
        ordering = ['id']

    id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_schedule_period_dates')
    #
    period_number = models.IntegerField(default=0)

    def __str__(self):
        return str(self.period_number)


class Period(models.Model):
    class Meta:
        verbose_name = _('period')
        verbose_name_plural = _('periods')

    id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_periods')
    #
    period_number = models.PositiveIntegerField(default=1)

    @property
    def is_current(self):
        return self.game.current_period == self.period_number

    @property
    def period(self):
        return self.game.start_period + self.period_number

    @property
    def name(self):
        return str(self.period)

    def __str__(self):
        return str(self.name)


class RandD(models.Model):
    class Meta:
        verbose_name = _('R and D Project')
        verbose_name_plural = _('R and D Projects')
        ordering = ['-period']

    id = models.AutoField(primary_key=True)
    period = models.ForeignKey(Period, null=True, on_delete=models.CASCADE, related_name='period_rds')
    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE, related_name='team_rds')
    segment = models.ForeignKey(Segment, null=True, on_delete=models.CASCADE, related_name='segment_rds')
    #
    scu_per_unit = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    prime_cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    project_expenditure = models.DecimalField(max_digits=18, decimal_places=2, default=1.00)
    #
    last_entered_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE,
                                        related_name='user_randds')
    #
    name = models.CharField(_('name'), blank=False, default='',
                            help_text=_('Please supply the R and D name.'), max_length=128)

    @property
    def product_id(self):
        try:
            rp = self.randd_products.all()[0]
            return rp.id
        except Exception as e:
            # print(e)
            return -1

    @property
    def product_name(self):
        try:
            rp = self.randd_products.all()[0]
            return rp.name
        except Exception as e:
            # print(e)
            return "Assign..."

    def get_or_create_product(self):
        try:
            # print('get_or_create_product 1')
            product = get_object_or_404(Product, team=self.team, randd=self)
            # print('get_or_create_product 2')
        except Exception as e:
            # print(e)
            product = Product.objects.create(team=self.team,
                                             randd=self,
                                             created_period=self.team.course_schedule.game.current_period_obj,
                                             name="PR-"+self.name)
            # print(10000)
            ppdd_randd = product.create_detail()
            ppdd_randd.amount = self.id
            # print(20000)
            # print('get_or_create_product 4')
            # print(product)
            # print('get_or_create_product 5')
        return product

    def save_model(self, request, obj, form, change):
        obj.last_entered_by = request.user
        obj.team = period.game.get_current_team(request.user)
        super().save_model(request, obj, form, change)

    def __str__(self):
        return str(self.name)


class RandD_Attribute(models.Model):
    class Meta:
        verbose_name = _('randd_attribute')
        verbose_name_plural = _('randd_attributes')
    id = models.AutoField(primary_key=True)
    #
    randd = models.ForeignKey(RandD, null=True, on_delete=models.CASCADE, related_name='randd_attributes')
    attribute = models.ForeignKey(Attribute, null=True, on_delete=models.CASCADE, related_name='attribute_randds')
    value = models.SmallIntegerField(default=0)
    #

    @property
    def index(self):
        # print(55555)
        op_ = self.attribute.get_period_optimal_value(self.randd.period.period_number)
        op = float(op_)
        v = float(self.value)
        c = v - op
        # print(op)
        # print(v)
        # print(c)
        if c>0:
            index = 1
        else:
            c = -c
            b = boltzman(c, 0, self.attribute.tau_miss_match)
            # print(b)
            index = np.round(1 - b + 0.5, 2)
        return index

    def __str__(self):
        return str(self.attribute.name)


class ManufacturingPeriodData(models.Model):
    class Meta:
        verbose_name = _('manufacturing data')
        verbose_name_plural = _('manufacturing data')

    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=None,
                                related_name='team_manufacturing')
    period = models.ForeignKey(Period, null=True, on_delete=models.CASCADE,
                               related_name='period_manufacturing_data')

    def create_detail(self):
        for t in self.team.course_schedule.game.game_type.manufacturing_attributes.all():
            try:
                mpdd = ManufacturingPeriodDataDetail.objects.create(manufacturing_data=self,
                                                                    manufacturing_type_attribute=t,
                                                                    amount=t.amount)
            except Exception as er:
                # pass
                print(er)

    def duplicate_detail(self):
        # print("manufacturing.duplicate_detail: " + self.team.name)
        game = self.team.course_schedule.game
        id_ = self.id
        mpdn = ManufacturingPeriodData.objects.get(id=id_)
        mpdn.pk = None
        mpdn.period = game.next_period_obj
        mpdn.save()
        mpd = ManufacturingPeriodData.objects.get(id=id_)
        for t in mpd.manufacturing_period_data_details.all():
            try:
                mpddn = ManufacturingPeriodDataDetail.objects.get(id=t.id)
                mpddn.pk = None
                mpddn.manufacturing_data = mpdn
                mpddn.save()
            except Exception as er:
                # print(er)
                pass

    def __str__(self):
        return "Manufacturing: "+str(self.period.period)


class ManufacturingPeriodDataDetail(models.Model):

    class Meta:
        verbose_name = _('manufacturing data detail')
        verbose_name_plural = _('manufacturing data details')
        ordering = ['id']

    id = models.AutoField(primary_key=True)
    amount = models.IntegerField(default=1)
    manufacturing_type_attribute = models.ForeignKey(ManufacturingTypeAttribute, default=None, null=True,
                                                     on_delete=models.CASCADE, related_name='attribute_mpdds')
    manufacturing_data = models.ForeignKey(ManufacturingPeriodData, null=True, on_delete=models.CASCADE,
                                           related_name='manufacturing_period_data_details')

    def __str__(self):
        return "Manufacturing: " + str(self.manufacturing_data.period.period) + " "+ str(self.type)


class HumanResourcesPeriodData(models.Model):
    class Meta:
        verbose_name = _('human resources data')
        verbose_name_plural = _('human resources data')

    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=None, related_name='team_human_resources')
    period = models.ForeignKey(Period, null=True, on_delete=models.CASCADE,
                               related_name='period_human_resources_data')

    def create_detail(self):
        for t in self.team.course_schedule.game.game_type.human_resources_attributes.all():
            try:
                hpdd = HumanResourcesPeriodDataDetail.objects.create(human_resources_data=self,
                                                                     human_resource_type_attribute=t,
                                                                     amount=t.amount)
            except Exception as er:
                # pass
                print(er)

    def duplicate_detail(self):
        print("HumanResources.duplicate_detail: " + self.team.name)
        game = self.team.course_schedule.game
        id_ = self.id
        hpdn = HumanResourcesPeriodData.objects.get(id=id_)
        hpdn.pk = None
        hpdn.period = game.next_period_obj
        hpdn.save()
        hpd = HumanResourcesPeriodData.objects.get(id=id_)
        for t in hpd.human_resources_period_data_details.all():
            try:
                hpddn = HumanResourcesPeriodDataDetail.objects.get(id=t.id)
                hpddn.pk = None
                hpddn.human_resources_data = hpdn
                hpddn.save()
            except Exception as er:
                # print(er)
                pass

    def __str__(self):
        return "HumanResources :" + str(self.period.period)


class HumanResourcesPeriodDataDetail(models.Model):

    class Meta:
        verbose_name = _('human resource data detail')
        verbose_name_plural = _('human resources data detail')
        ordering = ['id']

    id = models.AutoField(primary_key=True)
    amount = models.IntegerField(default=1)
    human_resource_type_attribute = models.ForeignKey(HumanResourcesTypeAttribute, default=None, null=True,
                                                      on_delete=models.CASCADE, related_name='attribute_hpdds')
    human_resources_data = models.ForeignKey(HumanResourcesPeriodData, null=True, on_delete=models.CASCADE,
                                             related_name='human_resources_period_data_details')

    def __str__(self):
        return "HumanResources: "+str(self.human_resource_type_attribute.name)


class Product(models.Model):
    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['-id']

    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_products')
    created_period = models.ForeignKey(Period, null=True, on_delete=models.CASCADE,
                                       related_name='created_period_products')
    abundant_period = models.ForeignKey(Period, null=True, on_delete=models.CASCADE,
                                        related_name='abundant_period_products')
    randd = models.ForeignKey(RandD, null=True, on_delete=models.CASCADE, related_name='randd_products')

    name = models.CharField(_('name'), null=True, default='',
                            help_text=_('Please supply the Product name.'), max_length=128)

    def set_abundant_period(self, p):
        self.abundant_period = p
        self.save()
        game = self.team.course_schedule.game
        ppd = self.product_periods_data.get(period=game.current_period_obj)
        for t in ProductPeriodDataDetail.TYPE:
            try:
                ppdt = ProductPeriodDataDetail.objects.get(product_data=ppd, type=t[0])
                ppdt.amount = 0
                ppdt.save()
            except Exception as er:
                # print(er)
                pass

    def duplicate_detail(self):
        game = self.team.course_schedule.game
        ppdn = self.product_periods_data.get(period=game.current_period_obj)
        ppdn.pk = None
        ppdn.period = game.next_period_obj
        ppdn.save()
        ppd = self.product_periods_data.get(period=game.current_period_obj)
        for t in ppd.product_period_data_details.all():
            try:
                ppddn = ProductPeriodDataDetail.objects.get(id=t.id)
                ppddn.pk = None
                ppddn.product_data = ppdn
                ppddn.save()
            except Exception as er:
                # print(er)
                pass

    def create_detail(self):
        game = self.team.course_schedule.game
        ppdd_randd = None
        try:
            ppd = self.product_periods_data.filter(period=game.current_period_obj)[0]
        except Exception as e:
            try:
                ppd = ProductPeriodData.objects.create(product_id=self.id, period=game.current_period_obj)
                for t in self.randd.segment.product_attributes.all():
                    try:
                        if self.abundant_period:
                            ppdd = ProductPeriodDataDetail.objects.create(product_data=ppd, product_type_attribute=t, amount=0)
                        else:
                            ppdd = ProductPeriodDataDetail.objects.create(product_data=ppd, product_type_attribute=t, amount=t.amount)
                            if(t.account_number==230):
                                ppdd_randd = ppdd
                    except Exception as er:
                        pass
                        # print(er)
            except Exception as er:
                pass
                # print(er)
        return ppdd_randd

    def __str__(self):
        return self.name


class ProductPeriodData(models.Model):
    class Meta:
        verbose_name = _('product data')
        verbose_name_plural = _('products data')

    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE,
                                related_name='product_periods_data')
    period = models.ForeignKey(Period, null=True, on_delete=models.CASCADE,
                               related_name='period_products_data')

    @property
    def advertisement(self):
        return self.product_period_data_details.filter(type < 100).aggregate(sum=Sum('amount'))

    @property
    def public_relation(self):
        return self.product_period_data_details.filter(type > 99).filter(type < 200).aggregate(sum=Sum('amount'))

    def __str__(self):
        return str(self.product.name)+":"+str(self.period.period)


class ProductPeriodDataDetail(models.Model):

    class Meta:
        verbose_name = _('product data detail')
        verbose_name_plural = _('products data detail')
        ordering = ['id']

    id = models.AutoField(primary_key=True)
    amount = models.IntegerField(default=1)
    product_type_attribute = models.ForeignKey(ProductTypeAttribute, default=None, null=True, on_delete=models.CASCADE,
                                               related_name='attribute_ppdds')
    product_data = models.ForeignKey(ProductPeriodData, null=True, on_delete=models.CASCADE,
                                     related_name='product_period_data_details')


class GDistributor(models.Model):
    class Meta:
        verbose_name = _('g_distributor')
        verbose_name_plural = _('g_distributors')
        ordering = ['-id']

    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_g_distributors')
    created = models.DateField(auto_now_add=True, null=True)
    distributor = models.ForeignKey(Distributor, null=True, on_delete=models.CASCADE, related_name='g_distributor')

    def create_detail(self):
        game = self.team.course_schedule.game
        try:
            dpd = self.g_distributor_periods_data.filter(period=game.current_period_obj)[0]
        except Exception as e:
            try:
                dpd = GDistributorPeriodData.objects.create(g_distributor_id=self.id, period=game.current_period_obj)
                for da in self.distributor.distributor_attributes.all():
                    try:
                        dpdd = GDistributorPeriodDataDetail.objects.create(g_distributor_data=dpd,
                                                                           distributor_attribute=da, amount=da.amount)
                    except Exception as er:
                        pass
            except Exception as er:
                pass
        return dpd

    def duplicate_detail(self):
        game = self.team.course_schedule.game
        dpdn = self.g_distributor_periods_data.get(period=game.current_period_obj)
        dpdn.pk = None
        dpdn.period = game.next_period_obj
        dpdn.save()
        dpd = self.g_distributor_periods_data.get(period=game.current_period_obj)

        for da in DistributorAttribute.objects.all():
            try:
                dpddn = GDistributorPeriodDataDetail.objects.get(g_distributor_data=dpd, distributor_attribute=da)
                dpddn.pk = None
                dpddn.g_distributor_data = dpdn
                dpddn.save()
            except Exception as er:
                # print(er)
                pass

    def __str__(self):
        return str(self.distributor.name)


class GDistributorPeriodData(models.Model):
    class Meta:
        verbose_name = _('g_distributor_data')
        verbose_name_plural = _('g_distributors_data')

    id = models.AutoField(primary_key=True)
    g_distributor = models.ForeignKey(GDistributor, null=True, on_delete=models.CASCADE,
                                      related_name='g_distributor_periods_data')
    period = models.ForeignKey(Period, null=True, on_delete=models.CASCADE,
                               related_name='period_g_distributors_data')

    @property
    def extra_support(self):
        return self.g_distributor_period_data_details.filter(type=110).aggregate(sum=Sum('amount'))

    def __str__(self):
        return str(self.g_distributor.distributor.name)+":"+str(self.period.period)


class GDistributorPeriodDataDetail(models.Model):

    class Meta:
        verbose_name = _('g_distributor_data_detail')
        verbose_name_plural = _('g_distributor_data_details')
        ordering = ['distributor_attribute']

    id = models.AutoField(primary_key=True)
    amount = models.IntegerField(default=1)
    g_distributor_data = models.ForeignKey(GDistributorPeriodData, null=True, on_delete=models.CASCADE,
                                           related_name='g_distributor_period_data_details')
    distributor_attribute = models.ForeignKey(DistributorAttribute, null=True, on_delete=models.CASCADE,
                                              related_name='g_distributor_attribute_period_data_details')


class Finance(models.Model):
    class Meta:
        verbose_name = _('finance')
        verbose_name_plural = _('finances')
        ordering = ['id']

    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_finances')
    created = models.DateField(auto_now_add=True, null=True)
    finance_type = models.ForeignKey(FinanceType, null=True, on_delete=models.CASCADE,
                                     related_name='finances')

    def create_detail(self):
        game = self.team.course_schedule.game
        try:
            fpd = self.finance_periods_data.filter(period=game.current_period_obj)[0]
        except Exception as e:
            try:
                fpd = FinancePeriodData.objects.create(finance_id=self.id, period=game.current_period_obj)
                for fa in self.finance_type.finance_attributes.all():
                    try:
                        # print(fa)
                        fpdd = FinancePeriodDataDetail.objects.create(finance_data=fpd,
                                                                      finance_attribute=fa, amount=fa.amount)
                    except Exception as er:
                        print(er)
                        # pass
            except Exception as err:
                print(err)
                # pass
        return fpd

    def duplicate_detail(self):
        game = self.team.course_schedule.game
        fpdn = self.finance_periods_data.get(period=game.current_period_obj)
        fpdn.pk = None
        fpdn.period = game.next_period_obj
        fpdn.save()
        fpd = self.finance_periods_data.get(period=game.current_period_obj)

        for t in fpd.finance_period_data_details.all():
            try:
                fpddn = FinancePeriodDataDetail.objects.get(id=t.id)
                fpddn.pk = None
                fpddn.finance_data = fpdn
                fpddn.save()
            except Exception as er:
                # print(er)
                pass

    def __str__(self):
        return str(self.finance_type.name)


class FinancePeriodData(models.Model):
    class Meta:
        verbose_name = _('finance_data')
        verbose_name_plural = _('finances_data')

    id = models.AutoField(primary_key=True)
    finance = models.ForeignKey(Finance, null=True, on_delete=models.CASCADE,
                                related_name='finance_periods_data')
    period = models.ForeignKey(Period, null=True, on_delete=models.CASCADE,
                               related_name='period_finances_data')

    def __str__(self):
        return str(self.finance.finance_type.name)+":"+str(self.period.period)


class FinancePeriodDataDetail(models.Model):

    class Meta:
        verbose_name = _('finance_data_detail')
        verbose_name_plural = _('finance_data_details')
        ordering = ['id']

    id = models.AutoField(primary_key=True)
    finance_data = models.ForeignKey(FinancePeriodData, null=True, on_delete=models.CASCADE,
                                     related_name='finance_period_data_details')
    finance_attribute = models.ForeignKey(FinanceTypeAttribute, null=True, on_delete=models.CASCADE,
                                          related_name='finance_type_periods_detail')
    amount = models.IntegerField(default=1)