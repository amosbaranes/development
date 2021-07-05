from django.contrib import admin
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'slug', 'created']
    list_filter = ['created']
