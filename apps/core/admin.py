from django.contrib import admin
from apps.core.models import Message, Question, UpDownVote, Room


class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'title_reunion', 'legislative_body_alias', 'youtube_id',
        'date', 'is_visible')
    list_filter = [
        'reunion_status', 'legislative_body_type', 'is_live', 'date']
    search_fields = (
        'title_reunion', 'legislative_body_initials', 'legislative_body_alias',
        'legislative_body', 'subcommission', 'location', 'cod_reunion')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'message', 'created')
    list_filter = ['user', 'room', 'created']
    search_fields = ['message']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'question', 'created')
    list_filter = ['user', 'room', 'created']
    search_fields = ['question']


class UpDownVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'created')
    list_filter = ['user', 'question', 'created']


admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UpDownVote, UpDownVoteAdmin)
