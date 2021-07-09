from django.contrib import admin
from .models import RadiusFoodWeb


@admin.register(RadiusFoodWeb)
class RadiusFoodWebAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', )



