from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from cms.models.fields import PlaceholderField
from filer.fields.image import FilerImageField


class Countries(models.Model):
    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')
        ordering = ['order']

    order = models.IntegerField(default=1000, blank=True)
    country_name = models.CharField(max_length=50, default='', blank=True)
    image_login_out = models.ImageField(upload_to='ugandatowns/countries/', blank=True, null=True,
                                        default='fab_hose_africa_web/no_image.png')
    image_login_in = models.ImageField(upload_to='ugandatowns/countries/', blank=True, null=True,
                                       default='fab_hose_africa_web/no_image.png')
    image_bg = models.ImageField(upload_to='ugandatowns/countries/', blank=True, null=True,
                                 default='fab_hose_africa_web/no_image.png')

    def __str__(self):
        return self.country_name


class Towns(models.Model):

    DISTRICT_TYPES = (
        (1, 'Central'),
        (2, 'Northern'),
        (3, 'Eastern'),
        (4, 'Central'),
    )

    class Meta:
        verbose_name = _('town')
        verbose_name_plural = _('towns')
        ordering = ['order']

    country = models.ForeignKey(Countries, models.SET_NULL, blank=True, null=True, related_name='towns')
    order = models.IntegerField(default=1000, blank=True)
    town_name = models.CharField(max_length=50, default='', blank=True)
    mayor = models.CharField(max_length=50, default='', blank=True)
    town_clerk = models.CharField(max_length=50, default='', blank=True)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    active = models.BooleanField(default=False)

    description = PlaceholderField('description', related_name='town_description')

    image = FilerImageField(blank=True, null=True, on_delete=models.SET_NULL, related_name='town_image')
    logo = FilerImageField(blank=True, null=True, on_delete=models.SET_NULL, related_name='town_logo')

    address1 = models.CharField(max_length=100, default='', blank=True)
    address2 = models.CharField(max_length=100, default='', blank=True)
    email = models.CharField(max_length=40, default='', blank=True)
    contact_us_email = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)

    media_ticker = models.CharField(max_length=20, default='', blank=True)

    slug = models.SlugField(_('slug'), blank=False, default='', db_index=True,
                            help_text=_('Please supply the town slug.'), max_length=128)

    bottom_info_color = models.CharField(max_length=10, default='blue', blank=True)
    menus_info_color = models.CharField(max_length=10, default='black', blank=True)

    def get_absolute_url(self):
        return reverse('ugandatowns:town', kwargs={'town_slug': self.slug, })

    def get_absolute_map_url(self):
        return reverse('ugandatowns:menu_town_other_model', kwargs={'town_slug': self.slug, 'html': 'contact_us'})

    def __str__(self):
        return self.town_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.town_name)
        super(Towns, self).save(*args, **kwargs)


class ReceivedMessages(models.Model):
    class Meta:
        verbose_name = _('received_message')
        verbose_name_plural = _('received_messages')

    town = models.ForeignKey(Towns, on_delete=models.CASCADE, related_name='received_messages')
    name = models.CharField(max_length=100, default='', blank=True)
    email = models.CharField(max_length=100, default='', blank=True)
    subject = models.CharField(max_length=100, default='', blank=True)
    message = models.CharField(max_length=2000, default='', blank=True)


class TownStaff(models.Model):

    POSITION_TYPES = (
        (0, 'Mayor'),
        (1, 'Town Clerk'),
        (2, 'Municipal Speaker'),
        (5, 'Accountant'),
        (10, 'Other'),
    )

    class Meta:
        verbose_name = _('town_staff')
        verbose_name_plural = _('town_staffs')

    town = models.ForeignKey(Towns, on_delete=models.CASCADE, related_name='town_staffs')
    position_type = models.IntegerField(default=10, choices=POSITION_TYPES)
    first_name = models.CharField(max_length=50, default='', blank=True)
    last_name = models.CharField(max_length=50, default='', blank=True)
    email = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    image = FilerImageField(blank=True, null=True, on_delete=models.SET_NULL, related_name='town_staff_image')


class Projects(models.Model):

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')
        ordering = ['order']

    order = models.IntegerField(default=1000, blank=True)
    town = models.ForeignKey(Towns, on_delete=models.CASCADE, related_name='town_projects')
    project_name = models.CharField(max_length=100, default='', blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    active = models.BooleanField(default=False)

    description = PlaceholderField('description')

    slug = models.SlugField(_('slug'), blank=False, default='', db_index=True,
                            help_text=_('Please supply the project slug.'), max_length=128)

    def get_absolute_url(self):
        return reverse('ugandatowns:menu_town_model', kwargs={
            'town_slug': self.town.slug, 'menu': 'projects', 'item_slug': self.slug, })

    def __str__(self):
        return self.town.town_name + ': ' + self.project_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.town + '-' + self.project_name)
        super(Projects, self).save(*args, **kwargs)


class Directors(models.Model):

    class Meta:
        verbose_name = _('director')
        verbose_name_plural = _('directors')
        ordering = ['order']

    order = models.IntegerField(default=1000, blank=True)
    town = models.ForeignKey(Towns, on_delete=models.CASCADE, related_name='town_directors')
    first_name = models.CharField(max_length=50, default='', blank=True)
    last_name = models.CharField(max_length=50, default='', blank=True)
    position = models.CharField(max_length=100, default='', blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    active = models.BooleanField(default=False)

    description = PlaceholderField('description')

    slug = models.SlugField(_('slug'), blank=False, default='', db_index=True,
                            help_text=_('Please supply the project slug.'), max_length=128)

    def get_absolute_url(self):
        return reverse('ugandatowns:menu_town_model', kwargs={
            'town_slug': self.town.slug, 'menu': 'directors', 'item_slug': self.slug, })

    def __str__(self):
        return self.town.town_name + ': ' + self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.town + '-' + self.first_name + '-' + self.last_name)
        super(Directors, self).save(*args, **kwargs)


class Services(models.Model):

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')
        ordering = ['order']

    order = models.IntegerField(default=1000, blank=True)
    town = models.ForeignKey(Towns, on_delete=models.CASCADE, related_name='town_services')

    service_name = models.CharField(max_length=100, default='', blank=True)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    active = models.BooleanField(default=False)

    description = PlaceholderField('description')

    slug = models.SlugField(_('slug'), blank=False, default='', db_index=True,
                            help_text=_('Please supply the service slug.'), max_length=128)

    def get_absolute_url(self):
        return reverse('ugandatowns:menu_town_model', kwargs={
            'town_slug': self.town.slug, 'menu': 'services', 'item_slug': self.slug, })

    def __str__(self):
        return self.town.town_name + ': ' + self.service_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.town + '-' + self.service_name)
        super(Services, self).save(*args, **kwargs)


class NewAnnouncements(models.Model):

    class Meta:
        verbose_name = _('newannouncement')
        verbose_name_plural = _('newannouncements')
        ordering = ['order']

    order = models.IntegerField(default=1000, blank=True)
    town = models.ForeignKey(Towns, on_delete=models.CASCADE, related_name='town_newannouncements')

    newannouncement_name = models.CharField(max_length=150, default='', blank=True)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    active = models.BooleanField(default=False)

    description = PlaceholderField('description')

    slug = models.SlugField(_('slug'), blank=False, default='', db_index=True,
                            help_text=_('Please supply the news or announcement slug.'), max_length=128)

    def get_absolute_url(self):
        return reverse('ugandatowns:menu_town_model', kwargs={
            'town_slug': self.town.slug, 'menu': 'newannouncements', 'item_slug': self.slug, })

    def __str__(self):
        return self.town.town_name + ': ' + self.newannouncement_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.town + '-' + self.newannouncement_name)
        super(NewAnnouncements, self).save(*args, **kwargs)


class Tenders(models.Model):

    class Meta:
        verbose_name = _('tender')
        verbose_name_plural = _('tenders')
        ordering = ['order']

    order = models.IntegerField(default=1000, blank=True)
    town = models.ForeignKey(Towns, on_delete=models.CASCADE, related_name='town_tenders')

    tender_name = models.CharField(max_length=150, default='', blank=True)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    active = models.BooleanField(default=False)

    description = PlaceholderField('description')

    slug = models.SlugField(_('slug'), blank=False, default='', db_index=True,
                            help_text=_('Please supply the tender slug.'), max_length=128)

    def get_absolute_url(self):
        return reverse('ugandatowns:menu_town_model', kwargs={
            'town_slug': self.town.slug, 'menu': 'tenders', 'item_slug': self.slug, })

    def __str__(self):
        return self.town.town_name + ': ' + self.tender_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.town + '-' + self.tender_name)
        super(Tenders, self).save(*args, **kwargs)


class Tourism(models.Model):

    class Meta:
        verbose_name = _('tourism')
        verbose_name_plural = _('tourism')
        ordering = ['order']

    order = models.IntegerField(default=1000, blank=True)
    town = models.ForeignKey(Towns, on_delete=models.CASCADE, related_name='town_tourism')

    tourism_name = models.CharField(max_length=150, default='', blank=True)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    active = models.BooleanField(default=False)

    description = PlaceholderField('description')

    slug = models.SlugField(_('slug'), blank=False, default='', db_index=True,
                            help_text=_('Please supply the tourism slug.'), max_length=128)

    def get_absolute_url(self):
        return reverse('ugandatowns:menu_town_model', kwargs={
            'town_slug': self.town.slug, 'menu': 'tourism', 'item_slug': self.slug, })

    def __str__(self):
        return self.town.town_name + ': ' + self.tourism_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.town + '-' + self.tourism_name)
        super(Tourism, self).save(*args, **kwargs)


class Careers(models.Model):

    class Meta:
        verbose_name = _('career')
        verbose_name_plural = _('careers')
        ordering = ['order']

    order = models.IntegerField(default=1000, blank=True)
    town = models.ForeignKey(Towns, on_delete=models.CASCADE, related_name='town_careers')

    career_name = models.CharField(max_length=150, default='', blank=True)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    active = models.BooleanField(default=False)

    description = PlaceholderField('description')

    slug = models.SlugField(_('slug'), blank=False, default='', db_index=True,
                            help_text=_('Please supply the career slug.'), max_length=128)

    def get_absolute_url(self):
        return reverse('ugandatowns:menu_town_model', kwargs={
            'town_slug': self.town.slug, 'menu': 'careers', 'item_slug': self.slug, })

    def __str__(self):
        return self.town.town_name + ': ' + self.career_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.town + '-' + self.career_name)
        super(Careers, self).save(*args, **kwargs)


class Conferencing(models.Model):

    class Meta:
        verbose_name = _('Conference')
        verbose_name_plural = _('Conferences')
        ordering = ['active', '-created_date']

    conference_number = models.AutoField(primary_key=True)
    conference_name = models.CharField(max_length=150, default='', blank=True)
    tc_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='town_conferences')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('ugandatowns:conference', kwargs={'conference_number': self.conference_number})

    def __str__(self):
        return str(self.conference_number) + ': ' + str(self.conference_name)


class ContactUs(models.Model):

    town = models.OneToOneField(Towns, on_delete=models.CASCADE, related_name='town_contact_us')
    description = PlaceholderField('description')

    def __str__(self):
        return self.town.town_name

