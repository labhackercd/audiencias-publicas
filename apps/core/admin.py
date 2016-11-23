from django.contrib import admin
from apps.core.models import Agenda, Message, Question, Video, UpDownVote


class AgendaAdmin(admin.ModelAdmin):
    list_display = ('commission', 'session', 'situation', 'date', 'created')
    list_filter = ['date', 'session', 'situation']


class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'message', 'created')
    list_filter = ['user', 'video', 'created']
    search_fields = ['message']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'question', 'created')
    list_filter = ['user', 'video', 'created']
    search_fields = ['question']


class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'closed_date', 'created')
    list_filter = ['created', 'closed_date']
    search_fields = ['title', 'description', 'videoId']


class UpDownVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'created')
    list_filter = ['user', 'question', 'created']


admin.site.register(Agenda, AgendaAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(UpDownVote, UpDownVoteAdmin)
