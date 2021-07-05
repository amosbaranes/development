from django.db import models
from django.urls import reverse


class BizlandWeb(models.Model):

    company_name = models.CharField(max_length=100, null=True)
    company_short_description = models.CharField(max_length=500, null=True)
    youtube_video_address = models.CharField(max_length=500, null=True)
    link_to_about_us = models.CharField(max_length=100, null=True)

    background_1 = models.ImageField(upload_to='bizland/',
                                     blank=True,
                                     null=True, default='fab_hose_africa_web/no_image.png')

    address1 = models.CharField(max_length=100, null=True)
    address2 = models.CharField(max_length=100, null=True)

    phone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=40, null=True)

    faq_title = models.CharField(max_length=100, null=True)
    faq_description = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.company_name


class Contact(models.Model):

    class Meta:
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'

    bizland_web = models.OneToOneField(BizlandWeb, null=True, on_delete=models.CASCADE, related_name='contact')
    title = models.CharField(max_length=100, default='', blank=True)
    information_title = models.CharField(max_length=100, default='', blank=True)
    send_message_title = models.CharField(max_length=100, default='', blank=True)
    contact_us_email = models.CharField(max_length=50, default='', blank=True)

    def __str__(self):
        return self.bizland_web.company_name


class Service(models.Model):

    class Meta:
        verbose_name = 'service'
        verbose_name_plural = 'services'

    bizland_web = models.ForeignKey(BizlandWeb, null=True, on_delete=models.CASCADE, related_name='services')
    icon = models.CharField(max_length=50, default='', blank=True)
    title = models.CharField(max_length=100, default='', blank=True)
    description = models.CharField(max_length=300, default='', blank=True)
    link_url_name = models.CharField(max_length=50, default='', blank=True)


class ReceivedMessages(models.Model):
    class Meta:
        verbose_name = 'received_message'
        verbose_name_plural = 'received_messages'

    contact = models.ForeignKey(Contact, null=True, on_delete=models.CASCADE, related_name='received_messages')
    name = models.CharField(max_length=100, default='', blank=True)
    email = models.CharField(max_length=100, default='', blank=True)
    subject = models.CharField(max_length=100, default='', blank=True)
    message = models.CharField(max_length=2000, default='', blank=True)


class Portfolio(models.Model):

    class Meta:
        verbose_name = 'portfolio'
        verbose_name_plural = 'portfolios'

    bizland_web = models.OneToOneField(BizlandWeb, null=True, on_delete=models.CASCADE, related_name='portfolio')
    title = models.CharField(max_length=100, default='', blank=True)
    description = models.CharField(max_length=300, default='', blank=True)

    def __str__(self):
        return str(self.bizland_web.company_name) + ': ' + str(self.title)


class PortfolioCategory(models.Model):

    class Meta:
        verbose_name = 'portfolio category'
        verbose_name_plural = 'portfolio categories'
    portfolio = models.ForeignKey(Portfolio, null=True, on_delete=models.CASCADE, related_name='portfolio_categories')
    name = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return str(self.portfolio) + ': ' + str(self.name)


class PortfolioItem(models.Model):

    class Meta:
        verbose_name = 'portfolio item'
        verbose_name_plural = 'portfolio items'

    portfolio_category = models.ForeignKey(PortfolioCategory, null=True, on_delete=models.CASCADE,
                                           related_name='portfolio_items')
    name = models.CharField(max_length=100, default='', blank=True)
    image = models.ImageField(upload_to='bizland/portfolio/', blank=True, null=True,
                              default='fab_hose_africa_web/no_image.png')

    def __str__(self):
        return self.name


class FAQ(models.Model):

    class Meta:
        ordering = ['id']

    company = models.ForeignKey(BizlandWeb, on_delete=models.CASCADE, related_name='faqs')
    title = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=500, null=True)

