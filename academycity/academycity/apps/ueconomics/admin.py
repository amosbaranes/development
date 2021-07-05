from django.contrib import admin
from .models import Source, Product, YearData


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['type']
    list_filter = ['type']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['sitc2', 'description']


@admin.register(YearData)
class YearDataAdmin(admin.ModelAdmin):
    list_display = ['source', 'product', 'year', 'value']
    list_filter = ['source', 'product']

