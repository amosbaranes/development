
from __future__ import unicode_literals
from django.contrib import admin
from .models import (InputFiles)

@admin.register(InputFiles)
class InputFilesAdmin(admin.ModelAdmin):
    list_display = ['title', 'file', 'user']


