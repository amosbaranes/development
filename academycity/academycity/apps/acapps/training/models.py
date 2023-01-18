from __future__ import unicode_literals
from django.db import models
from academycity.apps.core.sql import TruncateTableMixin


class TrainingWeb(TruncateTableMixin, models.Model):
    program_name = models.CharField(max_length=100, default='', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.program_name)


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
    brigade = models.ForeignKey(Brigades, on_delete=models.CASCADE, default=1, related_name='brigade_battalions')
    battalion_name = models.CharField(max_length=50, default='', blank=True, null=True)

    def __str__(self):
        return str(self.battalion_name)


# פלוגה/פלגה
class Companys(TruncateTableMixin, models.Model):
    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_companys')
    battalion = models.ForeignKey(Battalions, on_delete=models.CASCADE, default=1, related_name='battalion_companys')
    company_name = models.CharField(max_length=50, default='', blank=True, null=True)

    def __str__(self):
        return str(self.company_name)

# צוות
class Platoons(TruncateTableMixin, models.Model):
    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_sections')
    company = models.ForeignKey(Companys, on_delete=models.CASCADE, default=1, related_name='company_platoons')
    platon_name = models.CharField(max_length=50, default='', blank=True, null=True)

    def __str__(self):
        return str(self.section_name)

# כיתה
class Squads(TruncateTableMixin, models.Model):
    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_squads')
    platoon = models.ForeignKey(Platoons, on_delete=models.CASCADE, default=1, related_name='platoon_squads')
    squad_name = models.CharField(max_length=50, default='', blank=True, null=True)

    def __str__(self):
        return str(self.squad_name)

# חייל
class Soldiers(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'soldier'
        verbose_name_plural = 'soldiers'
        ordering = ['last_name']

    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_soldiers')
    squad = models.ForeignKey(Squads, on_delete=models.CASCADE, default=1, related_name='squad_soldiers')
    first_name = models.CharField(max_length=50, default='', blank=True, null=True)
    last_name = models.CharField(max_length=50, default='', blank=True, null=True)
    user_id = models.CharField(max_length=100, default='', blank=True, null=True)
    rank = models.SmallIntegerField(default=0)
    email = models.CharField(max_length=50, default='', blank=True, null=True)
    phone = models.CharField(max_length=50, default='', blank=True, null=True)
    address = models.CharField(max_length=100, default='', blank=True, null=True)
    country = models.CharField(max_length=50, default='', blank=True, null=True)
    state = models.CharField(max_length=50, default='', blank=True, null=True)
    city = models.CharField(max_length=50, default='', blank=True, null=True)
    blood_type =  models.CharField(max_length=10, default='', blank=True, null=True)

    birthday = models.DateField(blank=True, null=True)

    marital_status = models.SmallIntegerField(default=0)
    num_of_children = models.SmallIntegerField(default=0)
    shirt_size = models.SmallIntegerField(default=0)
    pant_size = models.SmallIntegerField(default=0)
    shoes_size = models.SmallIntegerField(default=0)
    height = models.SmallIntegerField(default=0)
    weight = models.SmallIntegerField(default=0)
    profession = models.SmallIntegerField(default=0)
    sub_profession = models.SmallIntegerField(default=0)

    # discipline = models.SmallIntegerField(default=0)
    # strength = models.SmallIntegerField(default=0)

    medical_condition = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.user_id) + ": " + str(self.first_name) + " " + str(self.last_name)


class DoubleShoot(TruncateTableMixin, models.Model):
    soldier = models.OneToOneField(Soldiers, on_delete=models.CASCADE, default=1,
                                   related_name='soldier_double_shoot')
    double_shoot_id = models.CharField(max_length=128, default='', blank=True, null=True)
    is_pulled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + ": " + str(self.double_shoot_id)


class TimeDim(TruncateTableMixin, models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    year = models.PositiveSmallIntegerField(default=0)
    month = models.PositiveSmallIntegerField(default=0)
    day = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.id)+" year="+str(self.year)


# class PlanningVsExecution(TruncateTableMixin, models.Model):


# class TestsDim(TruncateTableMixin, models.Model):
#     class Meta:
#         verbose_name = 'test'
#         verbose_name_plural = 'tests'
#
#     test_name = models.CharField(max_length=50, default='', blank=True, null=True)
#     test_content = models.JSONField(null=True)


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


# Safety
# professionalism
# Aggression

# פלגה
# צוות
# פק"ל אישי
# משמעת
# איתנות
# בעיות רפואיות - פרט

# מפקד
class Officer(TruncateTableMixin, models.Model):
    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_officers')
    first_name = models.CharField(max_length=50, default='', blank=True, null=True)
    last_name = models.CharField(max_length=50, default='', blank=True, null=True)
    email = models.CharField(max_length=50, default='', blank=True, null=True)
    phone = models.CharField(max_length=50, default='', blank=True, null=True)
    address = models.CharField(max_length=100, default='', blank=True, null=True)
    user_id = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return self.first_name+" "+self.last_name

