from django.contrib import admin
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from .models import (Countries, Towns, ReceivedMessages, TownStaff, Projects, Directors,
                     Services, NewAnnouncements, Tenders, Careers, Tourism, ContactUs, Conferencing)


class CountriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'country_name', )


admin.site.register(Countries, CountriesAdmin)


class TownsAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('town_name', 'order', 'mayor', 'town_clerk', 'active', 'country', )
    list_filter = ['country', ]

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('town_name',)}


admin.site.register(Towns, TownsAdmin)


class ProjectsAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('town', 'order', 'project_name', )

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('town', 'project_name',)}


admin.site.register(Projects, ProjectsAdmin)


class DirectorsAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('town', 'order', 'first_name', 'last_name', 'position', )

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('town', 'first_name', 'last_name',)}


admin.site.register(Directors, DirectorsAdmin)


class ServicesAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('town', 'order', 'service_name', )

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('town', 'service_name',)}


admin.site.register(Services, ServicesAdmin)


class NewAnnouncementsAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('town', 'order', 'newannouncement_name', )

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('town', 'newannouncement_name',)}


admin.site.register(NewAnnouncements, NewAnnouncementsAdmin)


class TownStaffAdmin(admin.ModelAdmin):
    list_display = ('town', 'first_name', 'last_name', 'email', 'phone', )


admin.site.register(TownStaff, TownStaffAdmin)


class ReceivedMessagesAdmin(admin.ModelAdmin):
    list_display = ('town', 'name', 'email', 'subject', )


admin.site.register(ReceivedMessages, ReceivedMessagesAdmin)


class TendersAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('town', 'order', 'tender_name', )

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('town', 'tender_name',)}


admin.site.register(Tenders, TendersAdmin)


class CareersAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('town', 'order', 'career_name', )

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('town', 'career_name',)}


admin.site.register(Careers, CareersAdmin)


class TourismAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('town', 'order', 'tourism_name', )

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('town', 'tourism_name',)}


admin.site.register(Tourism, TourismAdmin)


class ContactUsAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('town', 'id', )


admin.site.register(ContactUs, ContactUsAdmin)


class ConferencingAdmin(admin.ModelAdmin):
    list_display = ('conference_number', 'conference_name', 'tc_user', 'created_date', 'active', )
    list_filter = ['tc_user', 'created_date']


admin.site.register(Conferencing, ConferencingAdmin)
