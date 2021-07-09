from django.contrib import admin
from .models import (Service, Project,  PortfolioWeb)
from cms.admin.placeholderadmin import PlaceholderAdminMixin


@admin.register(PortfolioWeb)
class PortfolioWebAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'order', 'portfolio_name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'description', 'heading',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'heading', 'sub_heading', 'description')

