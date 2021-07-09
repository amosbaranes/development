from django.db import models
from filer.fields.image import FilerImageField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse


class RadiusFoodWeb(models.Model):

    class Meta:
        verbose_name = 'radius_food_web'
        verbose_name_plural = 'radius_food_webs'

    company_name = models.CharField(max_length=200, default='', blank=True)
    image_logo = models.ImageField(upload_to="radius_food_web", default="radius_food_web/no_image.png")
    office_address_1 = models.CharField(max_length=100, default='', blank=True)
    office_address_2 = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return self.company_name

