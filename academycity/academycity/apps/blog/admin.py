from __future__ import unicode_literals
from .models import Post, Comment
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
