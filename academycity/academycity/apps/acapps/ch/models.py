from django.db import models
from django.contrib.auth.models import User
from ...core.sql import TruncateTableMixin
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class ChWeb(TruncateTableMixin, models.Model):
    program_name = models.CharField(max_length=100, default='', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.program_name)


class Branches(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'branch'
        verbose_name_plural = 'branches'

    name = models.CharField(max_length=100, null=True, blank=True)
    branch_leader = models.ForeignKey('Members', on_delete=models.CASCADE, related_name='branches_members')

    def __str__(self):
        return self.name


class Departments(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'department'
        verbose_name_plural = 'departments'

    department_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.department_name


class BranchDepartments(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'department'
        verbose_name_plural = 'departments'

    department = models.ForeignKey(Departments, on_delete=models.CASCADE, related_name='branch_departments_department')
    branch = models.ForeignKey(Branches, on_delete=models.CASCADE, related_name='branch_departments_branch')
    department_leader = models.ForeignKey('Members', on_delete=models.CASCADE, related_name='departments_members')

    def __str__(self):
        return str(self.branch.name) + " " + str(self.department.name)


class Cells(models.Model):
    class Meta:
        verbose_name = 'cell'
        verbose_name_plural = 'cells'

    branch = models.ForeignKey(Branches, on_delete=models.CASCADE, blank=True, null=True)
    cell_leader = models.ForeignKey('Members', on_delete=models.CASCADE, related_name='cell_members')
    cell_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    cell_name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    cell_host = models.CharField(max_length=100, blank=True, null=True)
    meeting_day_and_time = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.cell_name


class Members(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'member'
        verbose_name_plural = 'members'
        ordering = ['-created']

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name='members')
    created = models.DateTimeField(auto_now_add=True)
    member_type = models.SmallIntegerField(default=0)
    gender = models.CharField(max_length=10,  null=True, blank=True)
    marital_status = models.BooleanField(default=True, null=True, blank=True)
    year_of_marriage = models.CharField(max_length=20, null=True, blank=True)
    has_children = models.BooleanField(default=True, null=True, blank=True)
    address = models.CharField(max_length=128, null=True, blank=True)
    occupation = models.CharField(max_length=128, null=True, blank=True)
    contact1 = models.CharField(max_length=50, null=True, blank=True)
    contact2 = models.CharField(max_length=50, null=True, blank=True)

    # members that just got borne again
    new_convert = models.BooleanField(default=False, null=True, blank=True)

    #  members that already completed a discipleship class and are serving in a certain department
    # class_attained = models.CharField(max_length=50, null=True, blank=True)
    # members who want to take a class
    # discipleship_class = models.ForeignKey('DiscipleshipClass', on_delete=models.CASCADE, null=True, blank=True)
    # discipleship_class_group = models.ForeignKey('CourseSchedule', on_delete=models.CASCADE, null=True, blank=True)

    department = models.ForeignKey(Departments, on_delete=models.CASCADE, null=True, blank=True)
    cell = models.ForeignKey(Cells, on_delete=models.CASCADE,  null=True, blank=True)
    branch = models.ForeignKey(Branches, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()


class Children(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'child'
        verbose_name_plural = 'children'

    member = models.ForeignKey(Members, on_delete=models.CASCADE, related_name='children_members')
    branch = models.ForeignKey(Branches, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)

