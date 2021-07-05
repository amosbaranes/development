# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.db import models
from django.utils.text import slugify
# from django.utils.encoding import python_2_unicode_compatible, force_text
from django.utils.translation import ugettext_lazy as _, get_language
from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import get_object_or_404
import math

# https://pypi.org/project/django-currentuser/
from django_currentuser.middleware import (get_current_user, get_current_authenticated_user)

from filer.fields.image import FilerImageField
from cms.models.fields import PlaceholderField
from parler.models import TranslatableModel, TranslatedFields
from parler.utils.context import switch_language

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation

from ..core.fields import OrderField
from ..actions.models import Action


# @python_2_unicode_compatible
class Department(TranslatableModel):
    class Meta:
        verbose_name = _('department')
        verbose_name_plural = _('departments')
        ordering = ['order']

    description = PlaceholderField('department_description')
    image = FilerImageField(blank=True, null=True, on_delete=models.SET_NULL)
    active = models.NullBooleanField(default=True)
    order = OrderField(blank=True, for_fields=[], default=1)

# upload_to='course/', default='course/unknown.png',

    translations = TranslatedFields(
        name=models.CharField(_('name'), blank=False, default='', db_index=True,
                              help_text=_('Please supply the department name.'), max_length=128),
        slug=models.SlugField(_('slug'), blank=False, default='', db_index=True,
                              help_text=_('Please supply the department slug.'), max_length=128)
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify('department-' + self.name + ' ' + get_language())
        super(Department, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     # Despite what the parler docs say, we need to add the extra parameter here.
    #     with switch_language(self, get_language()):
    #         try:
    #             print(reverse('courses:department_detail', kwargs={'slug': self.slug, }))
    #         except Exception as ee:
    #             print(ee)
    #         return reverse('courses:department_detail', kwargs={'slug': self.slug, })

    def __str__(self):
        return str(self.order) + ". " + self.name


# class OwnerManager(models.Manager):
#     def get_queryset(self):
#         return super(PublishedManager,
#                      self).get_queryset()\
#                           .filter(owner=request.user)
#
# class Post(models.Model):
#     # ...
# objects = models.Manager() # The default manager.
#     published = PublishedManager() # Our custom manager.


class Course(TranslatableModel):
    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')
        ordering = ['order']

    link_app = models.CharField(_('link_app'), blank=True, help_text=_('Please supply the link_app.'), max_length=50)
    link_model = models.CharField(_('link_model'), blank=True, help_text=_('Please supply the link_model.'), max_length=50)
    is_team = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='user_owns')
    description = PlaceholderField('course_description')
    image = FilerImageField(blank=True, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_courses')
    order = OrderField(blank=True, for_fields=['department'], default=1)
    active = models.NullBooleanField(default=True)
    instructors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        # limit_choices_to={'groups__id__in': get_user_model().objects.filter(groups__name="instructors").values_list('id', flat=True)},
        default=1, related_name='user_instructors')

    translations = TranslatedFields(
        name=models.CharField(_('name'), blank=False, default='', db_index=True,
                              help_text=_('Please supply the course name.'), max_length=128),
        slug=models.SlugField(_('slug'), blank=False, default='', db_index=True,
                              help_text=_('Please supply the course slug.'), max_length=128)
    )

    def get_absolute_url(self):
        with switch_language(self, get_language()):
            return reverse('courses:course_detail', kwargs={'slug': self.slug, })

    def get_course_view_url(self):
        with switch_language(self, get_language()):
            return reverse('courses:course_list_view', kwargs={'slug': self.slug, })

    def get_schedule_user_url(self):
        with switch_language(self, get_language()):
            return reverse('courses:get_registered_list', kwargs={'slug': self.slug, })

    def get_schedule_user_url1(self):
        with switch_language(self, get_language()):
            return reverse('courses:get_registered_list1', kwargs={'slug': self.slug, })

    def get_schedule_url(self):
        with switch_language(self, get_language()):
            return reverse('courses:register_form', kwargs={'slug': self.slug, })

    def get_create_blog_post_url(self):
        return reverse('blog:post_create', kwargs={})

    def get_blog_post_list_url(self):
        return reverse('blog:post_list', kwargs={})

    def get_registered_short_list1_url(self):
        return reverse('courses:get_registered_short_list1', kwargs={'slug': self.slug, })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.department.name + '-' + self.name + ' ' + get_language())
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.order) + ". " + self.name


# @python_2_unicode_compatible
class Syllabus(TranslatableModel):
    class Meta:
        verbose_name = _('syllabus')
        verbose_name_plural = _('syllabus')

    description = PlaceholderField('syllabus_description')
    image = FilerImageField(blank=True, null=True, on_delete=models.SET_NULL)
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='syllabus')

    translations = TranslatedFields(
        name=models.CharField(_('name'), blank=False, default='',
                              help_text=_('Please supply the syllabus name.'), max_length=128),
        slug=models.SlugField(_('slug'), blank=False, default='',
                              help_text=_('Please supply the syllabus slug.'), max_length=128)
    )

    def get_absolute_url(self):
        with switch_language(self, get_language()):
            print(self.slug)
            return reverse('courses:syllabus_detail', kwargs={'slug': self.slug, })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.course.name + '-' + self.name + ' ' + get_language())
            super(Syllabus, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# @python_2_unicode_compatible
class CourseSchedule(models.Model):

    ASSIGNMENT_METHOD = (
        (0, 'Other'),
        (1, 'Individual'),
        (2, 'Random'),
    )

    class Meta:
        verbose_name = _('course schedule')
        verbose_name_plural = _('courses schedule')
        ordering = ['-start_date']

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, default=1,
                              on_delete=models.CASCADE, related_name='user_course_schedule_owns')
    description = PlaceholderField('course_ schedule_description')
    image = FilerImageField(blank=True, null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_schedules')
    # add choice from the course instructors
    instructors = models.ManyToManyField(settings.AUTH_USER_MODEL, default=1, related_name='course_instructors')
    # how to assign students to teams?
    assignment_method = models.IntegerField(default=1, choices=ASSIGNMENT_METHOD)
    max_students_per_team = models.IntegerField(default=3)
    min_students_per_team = models.IntegerField(default=3)
    max_number_of_teams = models.IntegerField(default=7)
    min_number_of_teams = models.IntegerField(default=7)
    certificate_number = models.SmallIntegerField(default=1)

    created_date = models.DateField(auto_now_add=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    active = models.NullBooleanField(default=True)

    name = models.CharField(max_length=100, default='', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    target_ct = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE,
                                  related_name='course_schedule',
                                  limit_choices_to={'model__in': (
                                      'game',
                                      'project'
                                  )})

    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')

    slug = models.SlugField(_('slug'), blank=False, default='', db_index=True,
                            help_text=_('Please supply the course slug.'), max_length=128)

    @property
    def number_of_teams(self):
        return self.schedule_teams.count()

    @property
    def number_of_students_enrolled(self):
        return self.course_course_schedules.count()

    @property
    def number_of_students_assigned(self):
        return self.course_course_schedules.filter(team__isnull=False).count()

    @property
    def number_of_teams_left(self):
        free_places = 0
        assigned = 0
        available = 0
        for t in self.schedule_teams.all():
            assigned += t.number_of_members
            if self.min_students_per_team > t.number_of_members:
                free_places += (self.min_students_per_team - t.number_of_members)
                available += (self.max_students_per_team - self.min_students_per_team)
            else:
                available += (self.max_students_per_team - t.number_of_members)
        to_be_assigned = max(self.number_of_students_enrolled - assigned - free_places, 0)
        n_new = math.floor(to_be_assigned / self.min_students_per_team)
        n_left_students = max(to_be_assigned - n_new * self.min_students_per_team, 0)

        add_team = 1
        if n_left_students <= available:
            add_team = 0

        n_final = n_new + add_team
        return n_final

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.course.name + '-' + self.name)
        super(CourseSchedule, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('courses:course_schedule', kwargs={'slug': self.slug, })

    def get_simulation_url(self):
        return reverse(self.course.link_app + ':home', kwargs={'obj_id': self.target_id})

    def get_team_list_url1(self):
        return reverse('courses:get_team_list1', kwargs={'slug': self.slug, })

    def get_team_list_url2(self):
        return reverse('courses:get_team_list2', kwargs={'slug': self.slug, })

    def __str__(self):
        return self.name


class Team(models.Model):
    class Meta:
        verbose_name = _('team')
        verbose_name_plural = _('teams')
    course_schedule = models.ForeignKey(CourseSchedule, on_delete=models.CASCADE,
                                        null=True, related_name="schedule_teams")
    name = models.CharField(_('name'), blank=False, default='',
                            help_text=_('Please supply the team name.'), max_length=50)
    image = FilerImageField(blank=True, null=True, on_delete=models.SET_NULL)

    @property
    def number_of_members(self):
        return self.users.count()

    @property
    def status(self):
        if self.users.count() - self.course_schedule.max_students_per_team >= 0:
            return "full"
        elif self.users.count() - self.course_schedule.min_students_per_team >= 0:
            return "approved"
        return "missing"

    def __str__(self):
        return self.name


# @python_2_unicode_compatible
class CourseScheduleUser(models.Model):
    class Meta:
        verbose_name = _('course schedule user')
        verbose_name_plural = _('courses schedule user')
        ordering = ['course_schedule', 'team', 'user']

    course_schedule = models.ForeignKey(CourseSchedule, on_delete=models.CASCADE, related_name='course_course_schedules')
    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE, related_name="users")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_schedule_users')

    created_date = models.DateField(auto_now_add=True)
    active = models.NullBooleanField(default=False)
    graduated = models.NullBooleanField(default=False)
    paid = models.BooleanField(default=False)
    slug = models.SlugField(_('slug'), blank=False, default='', db_index=True,
                            help_text=_('Please supply the course slug.'), max_length=128)

    def get_user_name(self):
        return self.user.get_full_name()

    def get_absolute_url(self):
        return reverse('courses:course_schedule_user', kwargs={'slug': self.slug, })

    def get_diploma_url(self):
        return reverse('courses:get_diploma_pdf', kwargs={'slug': self.slug, })

    def __str__(self):
        return self.course_schedule.course.name + ': ' + self.user.get_full_name()


# @python_2_unicode_compatible
class Section(TranslatableModel):
    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')
        ordering = ['order']

    description = PlaceholderField('section_description')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_sections')
    order = OrderField(blank=True, for_fields=['course'], default=1)
    sections = GenericRelation(Action, related_query_name='sections')

    translations = TranslatedFields(
        name=models.CharField(_('name'), blank=False, default='', help_text=_('Please supply the section name.'), max_length=128),
        slug=models.SlugField(_('slug'), blank=True, default='', help_text=_('Please supply the section slug.'), max_length=128)
    )

    # def get_absolute_url(self):
    #     with switch_language(self, get_language()):
    #         return reverse('courses:section_detail', kwargs={'slug': self.slug, })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.course.name + '-' + self.name + ' ' + get_language())
        super(Section, self).save(*args, **kwargs)

    def get_edit_test_url(self):
        with switch_language(self, get_language()):
            return reverse('elearning:slug_edit_test_section', kwargs={'slug': self.course.slug, 'slug_section': self.slug, })

    def __str__(self):
        return str(self.order) + ". " + self.name


# @python_2_unicode_compatible
class SubSection(TranslatableModel):
    class Meta:
        verbose_name = _('sub_section')
        verbose_name_plural = _('sub_sections')
        ordering = ['order']

    description = PlaceholderField('sub_section_description')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='section_sub_sections')
    order = OrderField(blank=True, for_fields=['section'], default=1)
    actions = GenericRelation(Action, related_query_name='sub_sections')

    translations = TranslatedFields(
        name=models.CharField(_('name'), blank=False, default='', help_text=_('Please supply the sub section name.'), max_length=128),
        slug=models.SlugField(_('slug'), blank=False, default='', help_text=_('Please supply the sub section slug.'), max_length=128)
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.section.name + '-' + self.name + ' ' + get_language())
        super(SubSection, self).save(*args, **kwargs)

    def get_absolute_url(self):
        with switch_language(self, get_language()):
            return reverse('courses:slug_section', kwargs={'slug': self.section.course.slug, 'slug_section': self.slug, })

    # https://stackoverflow.com/questions/32795907/how-to-access-the-next-and-the-previous-elements-in-a-django-template-forloop

    # def get_next_url(self):
    #     with switch_language(self, get_language()):
    #         id = self.objects.filter(translations__language_code=get_language()).filter(section__slug=slug)
    #         x = self.objects.filter(translations__language_code=get_language()).filter(section__slug=slug).orderby('id')
    #         s_slug = x.filter(id>id)[0].slug
    #         return reverse('courses:slug_section', kwargs={'slug': self.section.course.slug, 'slug_section': s_slug, })

    def __str__(self):
        return self.name


# Orders
class Order(models.Model):
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ('-created',)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_order_users')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)

    def get_invoice_url(self):
        return reverse('courses:get_invoice_pdf', kwargs={'order_id': self.id})

    def get_payment_process_by_order_id_url(self):
        return reverse('courses:payment_process_', kwargs={'order_id': self.id})

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_price(self):
        return sum(item.total_price for item in self.items.all())

    def get_total_price_after_discount(self):
        return sum(item.total_price_after_discount for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(CourseSchedule, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    course_schedule_user_slug = models.SlugField(_('course_schedule_user_slug'), blank=False, default='', db_index=True,
                                                 help_text=_('Please supply the course slug.'), max_length=128)
    code = models.CharField(max_length=50, default='', blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price_after_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return '{}'.format(self.id)


# ------
# Coupon
# ------
class Coupon(models.Model):
    product = models.ForeignKey(CourseSchedule, related_name='coupon_items', on_delete=models.CASCADE)
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.code


# Accounting
# add parent child
# Handle currency
class ChartOfAccounts(TranslatableModel):
    class Meta:
        verbose_name = _('chart_of_account')
        verbose_name_plural = _('chart_of_accounts')

    code = models.CharField(max_length=10, default="0000000000")
    account_type = models.SmallIntegerField(default="2")

    parent = models.PositiveIntegerField(default=1)
    # took it from the Apphook doc: parent = models.ForeignKey('self', blank=True, null=True)
    # parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', default=1)

    translations = TranslatedFields(
        account=models.CharField(_('account'), blank=False, default='', db_index=True,
                                 help_text=_('Please supply the account name.'), max_length=128),
        slug=models.SlugField(_('slug'), blank=False, default='', db_index=True,
                              help_text=_('Please supply the department slug.'), max_length=128)
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(get_language() + '-' + self.account)
        super(ChartOfAccounts, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.account)


# @python_2_unicode_compatible
class GeneralLedger(models.Model):
    class Meta:
        verbose_name = _('general ledger')
        verbose_name_plural = _('general ledgers')

    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    target_ct = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_gl_obj', on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')

    transaction = models.PositiveIntegerField()
    sub_transaction = models.SmallIntegerField(default=1)
    account = models.ForeignKey(ChartOfAccounts, on_delete=models.CASCADE, related_name='cofa_gls')
    amount = models.DecimalField(max_digits=18, decimal_places=2)


# @python_2_unicode_compatible
class TrialBalance(models.Model):
    PERIOD_TYPES = (
        (0, 'Other'),
        (1, 'day'),
        (2, 'month'),
        (3, 'year'),
    )

    FLOW_TYPES = (
        (0, 'Other'),
        (1, 'flow'),
        (2, 'cumulative'),
    )

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    #
    # obj.get_period_type_display()
    period_type = models.IntegerField(default=1, choices=PERIOD_TYPES)
    flow_type = models.IntegerField(default=1, choices=FLOW_TYPES)
    pkey_date = models.IntegerField(default=0)
    account = models.ForeignKey(ChartOfAccounts, on_delete=models.CASCADE, related_name='cofa_tbs')
    amount = models.DecimalField(max_digits=18, decimal_places=2)


# -------------------------
# -------------------------
# @python_2_unicode_compatible
class Assignment(models.Model):

    ASSIGNMENT_TYPES = (
        (0, 'Other'),
        (1, 'Homework'),
        (2, 'Assignment'),
    )

    class Meta:
        verbose_name = _('assignment')
        verbose_name_plural = _('assignments')
    sub_section = models.ForeignKey(SubSection, on_delete=models.CASCADE, null=True, related_name='assignments')
    course_schedule = models.ForeignKey(CourseSchedule, on_delete=models.CASCADE, null=True,
                                        related_name='course_schedules_assignments')
    assignment_type = models.IntegerField(default=2, choices=ASSIGNMENT_TYPES)
    period_start = models.DateTimeField(null=True)
    period_end = models.DateTimeField(null=True)

    def get_assignment_user(self):
        owner_item = None
        if self.assignment_type == 1:
            print(get_current_user())
            assignment_user, n = AssignmentUser.objects.get_or_create(assignment=self, owner=get_current_user())
        elif self.assignment_type == 2:
            csu = get_object_or_404(CourseScheduleUser, course_schedule=self.course_schedule, user = get_current_user())
            assignment_user, n = AssignmentUser.objects.get_or_create(assignment=self, team_owner=csu.team)
        return assignment_user

    def __str__(self):
        return self.course_schedule.name + ' : ' + self.sub_section.section.name + ' : ' + self.sub_section.name


# @python_2_unicode_compatible
class AssignmentUser(models.Model):
    class Meta:
        verbose_name = _('assignment_user')
        verbose_name_plural = _('assignments_user')

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE,
                                   null=True, related_name='assignment_users')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE,
                              related_name='owner_assignments')
    team_owner = models.ForeignKey(Team, null=True, on_delete=models.CASCADE, related_name='team_owner_assignments')

    description = PlaceholderField('assignment_user_description')
    #
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def get_absolute_homework_url(self):
        with switch_language(self, get_language()):
            return reverse('courses:do_homework', kwargs={'slug': self.slug, })

    def get_absolute_assignment_url(self):
        with switch_language(self, get_language()):
            return reverse('courses:do_assignment', kwargs={'slug': self.slug, })


class AssignmentUserContent(models.Model):
    assignment_user = models.ForeignKey(AssignmentUser, on_delete=models.CASCADE, related_name='contents')
    #
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'text',
                                         'video',
                                         'image',
                                         'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    #
    order = OrderField(blank=True, for_fields=['assignment_user'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='user/assignments/files')


class Image(ItemBase):
    file = models.FileField(upload_to='user/assignments/images')


class Video(ItemBase):
    url = models.URLField()

