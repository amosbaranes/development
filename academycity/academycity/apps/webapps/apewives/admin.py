from django.contrib import admin
from .models import ApewivesWeb


@admin.register(ApewivesWeb)
class ApewivesWebAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', )

