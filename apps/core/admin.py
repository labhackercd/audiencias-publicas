from django.contrib import admin
from apps.core.models import Agenda, Message, Question, Video, UpDownVote


class AgendaAdmin(admin.ModelAdmin):
    list_display = ('commission', 'session', 'situation', 'date')
    list_filter = ['date', 'session', 'situation']


admin.site.register(Agenda, AgendaAdmin)
admin.site.register(Message)
admin.site.register(Question)
admin.site.register(Video)
admin.site.register(UpDownVote)
