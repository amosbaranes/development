from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from cms.admin.placeholderadmin import PlaceholderAdminMixin
from parler.admin import TranslatableAdmin, TranslatableStackedInline, TranslatableTabularInline

from .models import (Question, Answer)


class QuestionAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'active', )


class AnswerAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ('id', )


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
