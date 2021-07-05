from __future__ import unicode_literals
from .models import WebCompanies
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


@admin.register(WebCompanies)
class WebCompaniesAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'domain')
    # list_filter = ('status', 'created', 'publish', 'author')
    # search_fields = ('title', 'body')
    # prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ('author',)
    # date_hierarchy = 'publish'
    # ordering = ('status', 'publish')
