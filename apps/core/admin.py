from django.contrib import admin
from apps.core.models import Agenda, Message, Question, Video, UpDownVote, Room


class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'title_reunion', 'legislative_body_alias', 'youtube_id',
        'date', 'is_visible')
    list_filter = [
        'reunion_status', 'legislative_body_type', 'is_live', 'date']
    search_fields = (
        'title_reunion', 'legislative_body_initials', 'legislative_body_alias',
        'legislative_body', 'subcommission', 'location', 'cod_reunion')


class AgendaAdmin(admin.ModelAdmin):
    list_display = ('commission', 'session', 'situation', 'date', 'created')
    list_filter = ['date', 'session', 'situation']


class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'message', 'created')
    list_filter = ['user', 'room', 'created']
    search_fields = ['message']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'question', 'created')
    list_filter = ['user', 'room', 'created']
    search_fields = ['question']


class VideoAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'published_date', 'closed_date', 'created', 'room')
    list_filter = ['created', 'closed_date']
    search_fields = ['title', 'description', 'videoId']


class UpDownVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'created')
    list_filter = ['user', 'question', 'created']


admin.site.register(Room, RoomAdmin)
admin.site.register(Agenda, AgendaAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(UpDownVote, UpDownVoteAdmin)
