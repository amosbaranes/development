
from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from cms.admin.placeholderadmin import PlaceholderAdminMixin
from parler.admin import TranslatableAdmin, TranslatableStackedInline, TranslatableTabularInline

from .models import (Partners, Instructors, Publications)


class PartnersAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('owner', 'organization_name')


class InstructorsAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('user', )


class PublicationsAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'year', 'instructor')


admin.site.register(Partners, PartnersAdmin)
admin.site.register(Instructors, InstructorsAdmin)
admin.site.register(Publications, PublicationsAdmin)

