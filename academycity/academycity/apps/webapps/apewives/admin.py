from django.contrib import admin
from .models import ApewivesWeb, TitleSlides, SlidingImages, Team, Roadmap


@admin.register(ApewivesWeb)
class ApewivesWebAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', )


@admin.register(TitleSlides)
class TitleSlidesAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', )


@admin.register(SlidingImages)
class SlidingImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'image',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'team_header', 'team_description',)


@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ('id', 'text',)