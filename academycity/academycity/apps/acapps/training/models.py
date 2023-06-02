from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.utils import timezone
from academycity.apps.core.sql import TruncateTableMixin


class TrainingWeb(TruncateTableMixin, models.Model):
    program_name = models.CharField(max_length=100, default='', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.program_name)

# מדריכים
class Instructors(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'instructor'
        verbose_name_plural = 'instructors'
        ordering = ['last_name']
    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_instructors')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True,
                                related_name='training_user_instructors')
    default_battalion = models.IntegerField(default=1)
    first_name = models.CharField(max_length=50, default='', blank=True, null=True)
    last_name = models.CharField(max_length=50, default='', blank=True, null=True)
    position = models.SmallIntegerField(default=0)

    @property
    def full_name(self):
        return str(self.first_name) +": " + str(self.last_name)

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)

# חטיבה
class Brigades(TruncateTableMixin, models.Model):
    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_brigades')
    brigade_name = models.CharField(max_length=50, default='', blank=True, null=True)

    def __str__(self):
        return str(self.brigade_name)

# גדוד
class Battalions(TruncateTableMixin, models.Model):
    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_battalions')
    instructor = models.ManyToManyField(Instructors, default=[1],
                                        related_name='instructor_battalions')
    brigade = models.ForeignKey(Brigades, on_delete=models.CASCADE, default=1, related_name='brigade_battalions')
    battalion_name = models.CharField(max_length=50, default='', blank=True, null=True)
    battalion_number = models.SmallIntegerField(default=1)
    start_date = models.IntegerField(blank=True, null=True, default=20230101)
    number_of_weeks = models.SmallIntegerField(default=20)
    number_of_weeks_in_period_1 = models.SmallIntegerField(default=9)

    def __str__(self):
        return str(self.battalion_name)


class Periods(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'period'
        verbose_name_plural = 'periods'
        ordering = ['battalion', 'period_number']

    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_periods')
    battalion = models.ForeignKey(Battalions, on_delete=models.CASCADE, default=1, related_name='battalion_periods')
    period_number = models.SmallIntegerField(default=1)
    period_name = models.CharField(max_length=50, default='', blank=True, null=True)
    n_limit = models.SmallIntegerField(default=2)
    structure = models.JSONField(null=True)

    def __str__(self):
        return str(self.period_number) + ": " + str(self.period_name)

# פלוגה/פלגה
class Companys(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companys'
    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_companys')
    instructor = models.ManyToManyField(Instructors, default=[1],
                                        related_name='instructor_companys')
    company_number = models.SmallIntegerField(default=1)
    battalion = models.ForeignKey(Battalions, on_delete=models.CASCADE, default=1, related_name='battalion_companys')
    company_name = models.CharField(max_length=50, default='', blank=True, null=True)

    def __str__(self):
        return str(self.company_name)

# צוות
class Platoons(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'platoon'
        verbose_name_plural = 'platoons'
        ordering = ['company', 'platoon_number']

    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_platoons')
    instructor = models.ManyToManyField(Instructors, default=[1], related_name='instructor_platoons')
    platoon_number = models.SmallIntegerField(default=1)
    company = models.ForeignKey(Companys, on_delete=models.CASCADE, default=1, related_name='company_platoons')
    platoon_name = models.CharField(max_length=50, default='', blank=True, null=True)

    def __str__(self):
        return str(self.platoon_name)

# מחלקה
class Sections(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'section'
        verbose_name_plural = 'sections'
        ordering = ['platoon', 'section_name']
    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_sections')
    platoon = models.ForeignKey(Platoons, on_delete=models.CASCADE, null=True, related_name='platoon_sections')
    section_name = models.CharField(max_length=50, default='', blank=True, null=True)
    section_number = models.SmallIntegerField(default=1)

    @property
    def complete_name(self):
        return str(self.platoon.company.company_name) +": " + str(self.platoon.platoon_name) +": " + str(self.section_name)

    def __str__(self):
        return str(self.section_name)
# כיתה
class Squads(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'squad'
        verbose_name_plural = 'squads'
        ordering = ['platoon', 'squad_name']
    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_squads')
    platoon = models.ForeignKey(Platoons, on_delete=models.CASCADE, null=True, related_name='platoon_squads')
    squad_name = models.CharField(max_length=50, default='', blank=True, null=True)
    squad_number = models.SmallIntegerField(default=1)

    @property
    def complete_name(self):
        return str(self.platoon.company.company_name) +": " + str(self.platoon.platoon_name) +": " + str(self.squad_name)

    def __str__(self):
        return str(self.squad_name)

# קורסים
class Courses(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'course'
        verbose_name_plural = 'courses'
        ordering = ['course_name']
    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_courses')
    instructor = models.ManyToManyField(Instructors, default=[1],
                                        related_name='instructor_courses')
    course_name = models.CharField(max_length=50, default='', blank=True, null=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)

# Inventory
class InventoryCategorys(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'inventorycategory'
        verbose_name_plural = 'inventorycategorys'
        ordering = ['category_name']

    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_inventory_categorys')
    category_name = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return str(self.category_name)

class Inventorys(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'inventory'
        verbose_name_plural = 'inventorys'
        ordering = ['item_number']

    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_inventories')
    inventorycategory = models.ForeignKey(InventoryCategorys, on_delete=models.CASCADE, default=1,
                                          related_name='inventory_category_inventorys')
    pn = models.CharField(max_length=50, default='', blank=True, null=True)
    item_number = models.SmallIntegerField(default=0, blank=True, null=True)
    item_name = models.CharField(max_length=50, default='', blank=True, null=True)
    description = models.CharField(max_length=128, default='', blank=True, null=True)
    qty_per_soldier = models.SmallIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return str(self.item_name)

# חייל
class Soldiers(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'soldier'
        verbose_name_plural = 'soldiers'
        ordering = ['last_name']

    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_soldiers')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True,
                                related_name='user_training')
    battalion = models.ForeignKey(Battalions, on_delete=models.CASCADE, default=1, related_name='platoon_soldiers')
    platoon = models.ForeignKey(Platoons, on_delete=models.CASCADE, null=True, related_name='platoon_soldiers')
    course = models.ManyToManyField(Courses, default=[1], related_name='course_soldiers')
    #
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_confirmed = models.BooleanField(default=True)
    #
    first_name = models.CharField(max_length=50, default='', blank=True, null=True)
    last_name = models.CharField(max_length=50, default='', blank=True, null=True)
    image = models.ImageField(upload_to='training/%Y/%m/%d/', blank=True, null=True)
    userid = models.CharField(max_length=100, default='', blank=True, null=True)
    uniqueid = models.CharField(max_length=100, default='', blank=True, null=True)
    #
    shoes_size = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    clothes_size = models.CharField(max_length=2, default='', blank=True, null=True)
    #
    mz4psn = models.CharField(max_length=100, default='', blank=True, null=True)
    ramonsn = models.CharField(max_length=100, default='', blank=True, null=True)
    #
    address = models.CharField(max_length=100, default='', blank=True, null=True)
    city = models.CharField(max_length=50, default='', blank=True, null=True)
    state = models.CharField(max_length=50, default='', blank=True, null=True)
    zip = models.CharField(max_length=50, default='', blank=True, null=True)
    country = models.CharField(max_length=50, default='', blank=True, null=True)
    #
    email = models.CharField(max_length=50, default='', blank=True, null=True)
    phone = models.CharField(max_length=50, default='', blank=True, null=True)
    #
    birthday = models.DateField(blank=True, null=True)
    num_of_children = models.SmallIntegerField(default=0)
    marital_status = models.SmallIntegerField(default=0)
    #
    height = models.SmallIntegerField(default=0)
    weight = models.SmallIntegerField(default=0)
    blood_type =  models.CharField(max_length=10, default='', blank=True, null=True)
    #
    position = models.SmallIntegerField(default=0)
    rank = models.CharField(max_length=20, default='', blank=True, null=True)
    profession = models.SmallIntegerField(default=0)
    sub_profession = models.SmallIntegerField(default=0)
    #
    medical_condition = models.TextField(blank=True, null=True)
    #
    @property
    def full_name(self):
        return str(self.first_name) + " " + str(self.last_name)

    def __str__(self):
        return str(self.userid) + ": " + str(self.first_name) + " " + str(self.last_name)

class InventoryFact(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'inventory_fact'
        verbose_name_plural = 'inventory_facts'

    inventory = models.ForeignKey(Inventorys, on_delete=models.CASCADE, default=1,
                                  related_name='inventory_inventory_facts')
    soldier = models.ForeignKey(Soldiers, on_delete=models.CASCADE, default=1,
                                         related_name='soldier_inventory_facts')
    value = models.SmallIntegerField(default=0)

    def __str__(self):
        return str(self.inventory) + " : " + str(self.soldier) + " : " + str(self.value)

class UnitSoldiers(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'unit_soldier'
        verbose_name_plural = 'unit_soldiers'
        ordering = ['soldier', 'unit_number']

    period = models.ForeignKey(Periods, on_delete=models.CASCADE, default=1, related_name='period_unit_soldiers')
    soldier = models.ForeignKey(Soldiers, on_delete=models.CASCADE, default=1, related_name='soldier_unit_soldiers')
    unit_number = models.IntegerField(default=0)

    def __str__(self):
        return str(self.unit_number)+":"+str(self.soldier)

class TimeDim(TruncateTableMixin, models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    year = models.PositiveSmallIntegerField(default=0)
    month = models.PositiveSmallIntegerField(default=0)
    day = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.id)

#
class TestEvents(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'test_event'
        verbose_name_plural = 'test_events'

    instructor = models.ForeignKey(Instructors, on_delete=models.CASCADE, default=1,
                                   related_name='training_instructor_test_events')
    period = models.ForeignKey(Periods, on_delete=models.CASCADE, default=1,
                                 related_name='period_test_events')
    time_dim = models.ForeignKey(TimeDim, on_delete=models.CASCADE, default=1,
                                 related_name='time_dim_test_events')
    test_event_name = models.CharField(max_length=100, default='', blank=True, null=True)
    units_description = models.CharField(max_length=500, default='', blank=True, null=True)

    def __str__(self):
        return str(self.test_event_name)

class TestsForEvents(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'test_for_event'
        verbose_name_plural = 'test_for_events'

    testevent = models.ForeignKey(TestEvents, on_delete=models.CASCADE, default=1,
                                  related_name='test_event_tests_for_events')
    test_number = models.PositiveIntegerField(default=0)
    value = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.test_number)

class SoldiersForEvents(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'soldiers_for_event'
        verbose_name_plural = 'soldiers_for_events'

    testevent = models.ForeignKey(TestEvents, on_delete=models.CASCADE, default=1,
                                  related_name='test_event_soldiers_for_events')
    soldier_number = models.PositiveIntegerField(default=0)
    value = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.soldier_number)

class GradesForEvents(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'grades_for_event'
        verbose_name_plural = 'grades_for_events'

    testevent = models.ForeignKey(TestEvents, on_delete=models.CASCADE, default=1,
                                  related_name='test_event_grades_for_events')
    soldiersforevent = models.ForeignKey(SoldiersForEvents, on_delete=models.CASCADE, default=1,
                                         related_name='soldiersforevent_grades_for_events')
    testsforevent = models.ForeignKey(TestsForEvents, on_delete=models.CASCADE, default=1,
                                      related_name='testsforevent_grades_for_events')
    value = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return str(self.testevent)+"-"+str(self.soldiersforevent)+"-"+str(self.testsforevent)+"-"+str(self.value)

class TestsVariables(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'test_variable'
        verbose_name_plural = 'test_variables'

    variable_name = models.CharField(max_length=100, default='', blank=True, null=True)
    variable_description = models.CharField(max_length=500, default='', blank=True, null=True)
    up_value = models.SmallIntegerField(default=70)
    up_color = models.CharField(max_length=50, default='green', blank=True, null=True)
    down_value = models.SmallIntegerField(default=70)
    down_color = models.CharField(max_length=50, default='red', blank=True, null=True)
    other_color = models.CharField(max_length=50, default='yellow', blank=True, null=True)

    def __str__(self):
        return str(self.variable_name)

class TestsForVariables(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'test_for_variable'
        verbose_name_plural = 'test_for_variables'

    testsvariable = models.ForeignKey(TestsVariables, on_delete=models.CASCADE, default=1,
                                      related_name='test_variables_tests_for_variables')
    test_number = models.PositiveIntegerField(default=0)
    value = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    def __str__(self):
        return str(self.test_number)


# -- Compliance --
class ComplianceWeeks(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'compliance_week'
        verbose_name_plural = 'compliance_weeks'

    id = models.PositiveIntegerField(primary_key=True)
    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_compliance_weeks')
    battalion = models.ForeignKey(Battalions, on_delete=models.CASCADE, default=1, related_name='battalion_compliance_weeks')
    unit = models.IntegerField(blank=True, null=True)
    conclusion = models.TextField(blank=True, null=True)

class ComplianceDays(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'compliance_day'
        verbose_name_plural = 'compliance_days'

    compliance_week = models.ForeignKey(ComplianceWeeks, on_delete=models.CASCADE, default=1, related_name='compliance_week_compliance_days')
    time_dim = models.ForeignKey(TimeDim, on_delete=models.CASCADE, default=1, related_name='time_dim_compliance_days')
    time_unit = models.JSONField(null=True)


# SoldierQualificationFact
class SoldierQualificationFact(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'soldier_qualification_fact'
        verbose_name_plural = 'soldier_qualification_facts'

    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_soldier_qualification_facts')
    soldier = models.ForeignKey(Soldiers, on_delete=models.CASCADE, default=1,
                                related_name='soldier_soldier_qualification_facts')
    skill = models.SmallIntegerField(default=0)
    value = models.SmallIntegerField(default=0)

#
class DoubleShoot(TruncateTableMixin, models.Model):
    soldier = models.OneToOneField(Soldiers, on_delete=models.CASCADE, default=1,
                                   related_name='soldier_double_shoot')
    double_shoot_id = models.CharField(max_length=128, default='', blank=True, null=True)
    is_pulled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + ": " + str(self.double_shoot_id)


class DoubleShootMembers(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'double_shoot_member'
        verbose_name_plural = 'double_shoot_members'
        ordering = ['ds_id']

    ds_id = models.CharField(max_length=128, default='', blank=True, null=True)
    ds_name = models.CharField(max_length=128, default='', blank=True, null=True)
    data = models.JSONField(null=True)

    def __str__(self):
        return str(self.ds_name) + ": " + str(self.ds_id)

# class PlanningVsExecution(TruncateTableMixin, models.Model):

class SoldierFact(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'soldier_fact'
        verbose_name_plural = 'soldier_facts'

    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_soldier_facts')
    created = models.DateTimeField(auto_now_add=True, blank=True)
    time_dim = models.ForeignKey(TimeDim, on_delete=models.CASCADE, default=1,
                                 related_name='time_dim_soldier_facts')
    soldier = models.ForeignKey(Soldiers, on_delete=models.CASCADE, default=1,
                                related_name='soldier_soldier_facts')
    # test_dim = models.ForeignKey(TestsDim, on_delete=models.CASCADE, default=1,
    #                              related_name='test_dim_soldier_facts')
    test = models.SmallIntegerField(default=0)
    value = models.SmallIntegerField(default=0)


# -- Admin tables --
class ToDoList(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'todolist'
        verbose_name_plural = 'todolist'
        ordering = ['-is_active', 'priority', 'description']

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE,
                             related_name='training_user_todolists')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    subject = models.CharField(max_length=150, null=False)
    description = models.CharField(max_length=1000, null=False)
    priority = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.subject



# To Be Deleted ###
class TestsStructures(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'test_structure'
        verbose_name_plural = 'test_structures'
    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_tests')
    battalion = models.OneToOneField(Battalions, on_delete=models.CASCADE, primary_key=True,
                                     related_name='battalion_testsstructures')
    tests_structures_content = models.JSONField(null=True)

    def __str__(self):
        return str(self.battalion)

# ToBeDeleted
class Tests(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'test'
        verbose_name_plural = 'tests'

    soldier = models.ForeignKey(Soldiers, on_delete=models.CASCADE, default=1, related_name='soldier_tests')
    test = models.PositiveSmallIntegerField(default=0)
    grade = models.PositiveSmallIntegerField(default=0)
#