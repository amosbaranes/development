from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _, get_language


class Image(models.Model):
    CATEGORY_CHOICES = (
        (0, _('General')),
        (5, _('Data Science')),
        (10, _('Finance')),
        (15, _('Business Intelligence')),
        (20, _('Machine Learning')),
        (25, _('Business Simulation')),
        (30, _('Partners')),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.SmallIntegerField(default=0, choices=CATEGORY_CHOICES)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    # image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)

    def get_absolute_url(self):
            return reverse('images:detail', args=[self.id, self.slug])
