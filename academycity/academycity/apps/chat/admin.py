from django.contrib import admin

from .models import Thread, ChatMessage, Whiteboard, WhiteboardData


@admin.register(Whiteboard)
class WhiteboardAdmin(admin.ModelAdmin):
    list_display = ['id', 'board_name']


@admin.register(WhiteboardData)
class WhiteboardDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'color', 'xf', 'yf', 'xt', 'yt', 'mode', 'pen_size', 'painter', 'whiteboard']


class ChatMessage(admin.TabularInline):
    model = ChatMessage


class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]

    class Meta:
        model = Thread


admin.site.register(Thread, ThreadAdmin)