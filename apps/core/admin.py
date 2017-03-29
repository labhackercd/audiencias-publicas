from django.contrib import admin
from apps.core.models import Agenda, Message, Question, Video, UpDownVote, Room


class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'get_comission', 'get_session', 'get_situation',
        'get_video', 'is_visible')
    list_filter = ['is_visible', 'agenda__situation', 'agenda__session']
    search_fields = (
        'agenda__commission', 'agenda__session', 'agenda__situation',
        'agenda__date', 'agenda__created', 'video__title', 'video__videoId')

    def get_video(self, obj):
        if obj.video:
            return obj.video.videoId
        else:
            return 'Sem vídeo'

    def get_comission(self, obj):
        if obj.agenda:
            return obj.agenda.commission
        else:
            return 'Sala não agendada'

    def get_session(self, obj):
        if obj.agenda:
            return obj.agenda.session
        else:
            return 'Sala não agendada'

    def get_situation(self, obj):
        if obj.agenda:
            return obj.agenda.situation
        else:
            return 'Sala não agendada'

    get_video.short_description = 'Vídeo'
    get_comission.short_description = 'Comissão'
    get_session.short_description = 'Sessão'
    get_situation.short_description = 'Situação'


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
