from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from filer.fields.image import FilerImageField
# from ckeditor.fields import RichTextField  # ,
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import ugettext_lazy as _, get_language


class Institution(models.Model):
    TYPES = (
        (0, 'Other'),
        (1, 'University'),
        (2, 'College'),
        (3, 'Company'),
        (4, 'Private'),
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, default='', blank=True)
    type = models.IntegerField(default=1, choices=TYPES)

    def get_absolute_url(self):
        return reverse('users:detailed_institution', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Profile(models.Model):
    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
        ordering = ['-created']

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_confirmed = models.BooleanField(default=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                primary_key=True, related_name='academics')
    short_bio = RichTextUploadingField(_('short_bio'), blank=True, null=True)
    bio = RichTextUploadingField(_('bio'), blank=True, null=True)
    #
    address = models.CharField(_('address'), max_length=128, default='', blank=True)
    zip = models.CharField(_('zip'), max_length=20, default='', blank=True)
    city = models.CharField(_('city'), max_length=100, default='', blank=True)
    country = models.CharField(_('country'), max_length=100, default='', blank=True)
    #
    phone = models.CharField(_('phone'), max_length=20, default='', blank=True)
    website = models.URLField(_('website'), default='http://academycity.org', blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    institution = models.ForeignKey(Institution, null=True, blank=True, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()

