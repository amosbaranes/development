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
