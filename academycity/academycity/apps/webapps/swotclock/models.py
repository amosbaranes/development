from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class SWOTClock(models.Model):
    swot_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE,
                                  related_name='user_swot_clocks')
    file_name = models.CharField(max_length=100, default='swot', blank=True)

    def __str__(self):
        return self.swot_user.first_name + ' ' + self.swot_user.last_name + ': ' + self.file_name


class SWOTClockData(models.Model):
    swot_clock = models.ForeignKey(SWOTClock, null=True, on_delete=models.CASCADE, related_name='swot_clock_data')
    field_id = models.CharField(max_length=60, default='', blank=True)
    field_value = models.CharField(max_length=50, default='', blank=True)


