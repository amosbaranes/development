from django.contrib import admin
from .models import (InstitutionWeb, Course, New, Program, Subject, Person, Phrase, AdditionalTopic,
                     MoreNewsDetail, Services)
from cms.admin.placeholderadmin import PlaceholderAdminMixin


@admin.register(InstitutionWeb)
class InstitutionWebAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'institution_name', 'domain_name', 'email', 'phone', )


@admin.register(Course)
class CourseAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'order', 'name', 'date', 'is_popular', 'is_active', )
    list_filter = ('is_active', 'is_popular', )


@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'news_title', 'news_description', 'news_date', 'is_popular', 'is_active')
    list_filter = ('is_active', 'is_popular', )


@admin.register(Program)
class ProgramAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'order', 'name', 'short_description', 'is_popular', )
    list_filter = ('is_active', 'is_popular', )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'subject_name', 'is_popular', 'is_active',)
    list_filter = ('is_active', 'is_popular', )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'persons_name', 'persons_description', 'is_popular', 'is_active',)
    list_filter = ('is_active', 'is_popular', )


@admin.register(Phrase)
class PhraseAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'image', 'persons_phrase', 'is_active')


@admin.register(AdditionalTopic)
class PhraseAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'image', 'topic_description', 'is_link', 'is_active')


@admin.register(MoreNewsDetail)
class MoreNewsDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'news_title', 'news_description', 'news_date', 'is_popular', 'is_active')
    list_filter = ('is_active', 'is_popular', )


@admin.register(Services)
class ServicesAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'order', 'name', 'short_description',)
    list_filter = ('is_active',)
