from django.db import models
from django.contrib.auth.models import User
from ...core.sql import TruncateTableMixin
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


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
    cell_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    cell_name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    cell_leader = models.ForeignKey('Members', on_delete=models.CASCADE, related_name='cell_members')

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
    branch = models.ForeignKey(Branches, null=True, blank=True, on_delete=models.CASCADE)

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


# ========== COURSES ========
class Courses(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'course'
        verbose_name_plural = 'courses'
        ordering = ['order']

    order = models.IntegerField(default=1000, blank=True)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=128, blank=False, default='', db_index=True)
    content = models.TextField()

    def __str__(self):
        return self.name


class CourseSchedule(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'course_schedule'
        verbose_name_plural = 'courses_schedules'
        ordering = ['-start_date']

    order = models.IntegerField(default=1000, blank=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='course_schedules')
    instructors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='course_schedule_instructors')
    created_date = models.DateField(auto_now_add=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    active = models.BooleanField(default=True)

    name = models.CharField(max_length=100, null=True, blank=True)

    @property
    def number_of_students_enrolled(self):
        return self.courses_course_schedules.count()

    @property
    def number_of_students_active(self):
        active_users_count = CourseScheduleUser.objects.filter(course_schedule=self, active=True).count()
        return active_users_count

    def save(self, *args, **kwargs):
        super(CourseSchedule, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class CourseScheduleUser(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'course_schedule_user'
        verbose_name_plural = 'courses_schedule_users'
        ordering = ['course_schedule', 'user']

    course_schedule = models.ForeignKey(CourseSchedule, on_delete=models.CASCADE,
                                        related_name='courses_course_schedules')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses_schedule_users')

    created_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=False)
    graduated = models.BooleanField(default=False)

    def get_user_name(self):
        return self.user.get_full_name()

    def __str__(self):
        return self.course_schedule.course.name + ': ' + self.user.get_full_name()


# ============== SERVICE =============
class Services(models.Model):
    class Meta:
        verbose_name = 'service'
        verbose_name_plural = 'services'
        ordering = ['order']

    order = models.IntegerField(default=100, blank=True)
    branch = models.ForeignKey(Branches, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateField()
    content = models.TextField()

    def __str__(self):
        return f"{self.name} on {self.date}"


class ServiceCalenders(models.Model):
    class Meta:
        verbose_name = 'service_calender'
        verbose_name_plural = 'service_calenders'
        ordering = ['order']

    name = models.CharField(max_length=255)
    branch = models.ForeignKey(Branches, null=True, blank=True, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.name} on {self.date}"


class ServiceAttendance(models.Model):
    class Meta:
        verbose_name = 'service_attendance'
        verbose_name_plural = 'service_attendances'

    service_calender = models.ForeignKey(ServiceCalenders, on_delete=models.CASCADE,
                                         related_name='service_attendance_services_calender')
    member = models.ForeignKey(Members, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.member.user.get_full_name()} attended {self.service.name} on {self.service_calender.date}"


# ======== END OF SERVICE =========


# ========= CHURCH EVENTS ==========
class Events(models.Model):
    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'
        ordering = ['order']

    order = models.IntegerField(default=100, blank=True)
    branch = models.ForeignKey(Branches, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255, blank=True, null=True)

    # capitalize the first letter of event name
    def __str__(self):
        return f"{self.name} on {self.date}"


class EventAttendance(models.Model):
    class Meta:
        verbose_name = 'event_attendance'
        verbose_name_plural = 'event_attendances'

    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='event_attendance')
    member = models.ForeignKey(Members, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.member.user.get_full_name()} attended {self.event.name} on {self.event.date}"


# ========= END OF CHURCH EVENTS ==============


# ========== CONTRIBUTION ==================
class ContributionCategorys(models.Model):
    class Meta:
        verbose_name = 'contribution_category'
        verbose_name_plural = 'contribution_categorys'
        ordering = ['order']

    order = models.IntegerField(default=100, blank=True)
    name = models.CharField(max_length=128, unique=True)
    branch = models.ForeignKey(Branches, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Contribution(models.Model):
    class Meta:
        verbose_name = 'contribution'
        verbose_name_plural = 'contributions'

    contribution_category = models.ForeignKey(ContributionCategorys, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    contributor = models.ForeignKey('Members', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.contribution_category.name} - {self.amount} on {self.date}"


# ========== END OF CONTRIBUTION ==================


# ============== EXPENSE ==============
class ExpenseCategorys(models.Model):
    class Meta:
        verbose_name = 'expense_category'
        verbose_name_plural = 'expense_categorys'
        ordering = ['order']

    order = models.IntegerField(default=100, blank=True)
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    class Meta:
        verbose_name = 'expense'
        verbose_name_plural = 'categorys'

    branch = models.ForeignKey(Branches, null=True, blank=True, on_delete=models.CASCADE)
    expense_category = models.ForeignKey(ExpenseCategorys, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)
    comment = models.TextField()

    def __str__(self):
        return f"{self.expense_category.name} - {self.amount} on {self.date}"

# ============== END OF EXPENSE ==============
