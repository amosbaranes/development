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
class Sections(TruncateTableMixin, models.Model):
    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_sections')
    company = models.ForeignKey(Companys, on_delete=models.CASCADE, default=1, related_name='company_sections')
    section_name = models.CharField(max_length=50, default='', blank=True, null=True)

    def __str__(self):
        return str(self.section_name)


# כיתה
class Squads(TruncateTableMixin, models.Model):
    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_squads')
    section = models.ForeignKey(Sections, on_delete=models.CASCADE, default=1, related_name='section_squads')
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
    discipline = models.SmallIntegerField(default=0)
    strength = models.SmallIntegerField(default=0)
    medical_condition = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.user_id) + str(self.first_name) + " " + str(self.last_name)


class PrivateSpecialty(TruncateTableMixin, models.Model):
    class Meta:
        verbose_name = 'private_speciality'
        verbose_name_plural = 'private_specialities'
        ordering = ['last_name']

    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_private_specialties')
    soldier = models.ForeignKey(Squads, on_delete=models.CASCADE, default=1, related_name='soldier_private_specialties')
    specialty = models.SmallIntegerField(default=0)
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
class Officer (TruncateTableMixin, models.Model):
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

