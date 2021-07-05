from django.db import models
from filer.fields.image import FilerImageField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation


class WebCompanies(models.Model):

    class Meta:
        verbose_name = 'web_companies'
        verbose_name_plural = 'web_companies'

    company_name = models.CharField(max_length=200, default='', blank=True)
    domain = models.CharField(max_length=100, default='', blank=True)
    created_date = models.DateField(auto_now_add=True)

    target_ct = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE,
                                  related_name='webcompanies',
                                  limit_choices_to={'model__in': (
                                      'fabhoseafricaweb',
                                      'bizlandweb',
                                      'radiusfoodweb',
                                      'countries',
                                      'institutionweb',
                                      'checkcashingweb'
                                  )})

    target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')

    #
    # @property
    # def number_of_teams(self):
    #     return self.schedule_teams.count()

    def __str__(self):
        return self.company_name
