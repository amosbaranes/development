from django.db import models
from django.conf import settings
from ..core.fields import OrderField
from ..users.models import Institution
from cms.models.fields import PlaceholderField
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager


class Partners(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='partners')
    order = OrderField(blank=True, for_fields=[], default=1)
    organization_name = models.CharField(max_length=128, default='')
    address1 = models.CharField(max_length=128, blank=True, null=True)
    address2 = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField()
    city = models.CharField(max_length=128, default='')
    country = models.CharField(max_length=128, default='')
    office_phone = models.CharField(max_length=128, default='')
    cell_phone = models.CharField(max_length=128, default='')
    owner_image = models.ImageField(upload_to='partners/%Y/%m/%d/', blank=True, null=True)
    organization_image = models.ImageField(upload_to='partners/%Y/%m/%d/', blank=True, null=True)
    description = PlaceholderField('partner_description')
    slug = models.SlugField(max_length=250, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.owner.get_full_name() + '-' + self.id)
        super(Partners, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('partners:partner_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.owner.get_full_name()


class Instructors(models.Model):
    class Meta:
        ordering = ['order']
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructors')
    order = models.IntegerField(blank=True, default=10000)
    institution = models.ManyToManyField(Institution, blank=True, related_name="institution_instructors")
    short_bio = PlaceholderField('partner_short_bio', related_name="short_bio")
    full_bio = PlaceholderField('partner_full_bio', related_name="full_bio")
    tags = TaggableManager()
    slug = models.SlugField(max_length=250, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.get_full_name() + '-' + self.id)
        super(Instructors, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('instructors:instructor', kwargs={'slug': self.slug})

    def __str__(self):
        return self.user.get_full_name()


class Publications(models.Model):
    class Meta:
        ordering = ['-year', 'order']

    instructor = models.ForeignKey(Instructors, on_delete=models.CASCADE,
                                   related_name='publications')
    order = OrderField(blank=True, for_fields=[], default=1)
    title = models.CharField(max_length=128, default='')
    publisher = models.CharField(max_length=128, default='')
    year = models.SmallIntegerField(default='2020')
    citation = models.CharField(max_length=256, default='')

    def __str__(self):
        return self.citation

