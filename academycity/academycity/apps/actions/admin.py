from django.contrib import admin
from .models import Action, ActionSubCategory, ActionCategory


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'verb', 'target', 'created')
    list_filter = ('created',)
    search_fields = ('verb',)

@admin.register(ActionCategory)
class ActionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ActionSubCategory)
class ActionSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('category',)
