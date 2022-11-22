from __future__ import unicode_literals
from django.db import models
from academycity.apps.core.sql import TruncateTableMixin


class TrainingWeb(TruncateTableMixin, models.Model):
    program_name = models.CharField(max_length=100, default='', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    number_of_periods = models.SmallIntegerField(default=9)
    number_of_participants = models.SmallIntegerField(default=9)
    number_of_teams = models.SmallIntegerField(default=7)
    max_participants_in_team = models.SmallIntegerField(default=6)

    def __str__(self):
        return str(self.program_name)


# חטיבה
class Brigades(TruncateTableMixin, models.Model):
    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_brigades')
    brigade_name = models.CharField(max_length=50, default='', blank=True, null=True)


# גדוד
class Battalions(TruncateTableMixin, models.Model):
    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_battalions')
    brigade = models.ForeignKey(Brigades, on_delete=models.CASCADE, default=1,
                                related_name='brigade_battalions')
    battalion_name = models.CharField(max_length=50, default='', blank=True, null=True)


# פלוגה/פרגה
class Companys(TruncateTableMixin, models.Model):
    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_companys')
    battalion = models.ForeignKey(Battalions, on_delete=models.CASCADE, default=1,
                                  related_name='battalion_companys')
    company_name = models.CharField(max_length=50, default='', blank=True, null=True)


# צוות
class Sections(TruncateTableMixin, models.Model):
    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_sections')
    company = models.ForeignKey(Companys, on_delete=models.CASCADE, default=1,
                                related_name='company_sections')
    section_name = models.CharField(max_length=50, default='', blank=True, null=True)


# כיתה
class Squads(TruncateTableMixin, models.Model):
    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_squads')
    section = models.ForeignKey(Sections, on_delete=models.CASCADE, default=1,
                                related_name='section_squads')
    squad_name = models.CharField(max_length=50, default='', blank=True, null=True)


# חייל
class Solders(TruncateTableMixin, models.Model):
    training_web = models.ForeignKey(TrainingWeb, on_delete=models.CASCADE, default=1,
                                     related_name='training_web_solders')
    squad = models.ForeignKey(Squads, on_delete=models.CASCADE, default=1,
                              related_name='squad_solders')
    first_name = models.CharField(max_length=50, default='', blank=True, null=True)
    last_name = models.CharField(max_length=50, default='', blank=True, null=True)
    email = models.CharField(max_length=50, default='', blank=True, null=True)
    phone = models.CharField(max_length=50, default='', blank=True, null=True)
    address = models.CharField(max_length=100, default='', blank=True, null=True)
    user_id = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return self.first_name+" "+self.last_name


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

