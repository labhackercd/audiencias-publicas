from django.contrib import admin
from apps.reports.models import (NewUsers, VotesReport, RoomsReport,
                                 QuestionsReport, MessagesReport,
                                 ParticipantsReport)


class NewUsersAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'new_users', 'created')
    list_filter = ['start_date', 'period']


class VotesReportAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'votes', 'created')
    list_filter = ['start_date', 'period']


class RoomsReportAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'finished_rooms', 'canceled_rooms',
                    'total_rooms', 'created')
    list_filter = ['start_date', 'period']


class QuestionsReportAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'questions', 'created')
    list_filter = ['start_date', 'period']


class MessagesReportAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'messages', 'created')
    list_filter = ['start_date', 'period']


class ParticipantsReportAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'participants', 'created')
    list_filter = ['start_date', 'period']


admin.site.register(NewUsers, NewUsersAdmin)
admin.site.register(VotesReport, VotesReportAdmin)
admin.site.register(RoomsReport, RoomsReportAdmin)
admin.site.register(QuestionsReport, QuestionsReportAdmin)
admin.site.register(MessagesReport, MessagesReportAdmin)
admin.site.register(ParticipantsReport, ParticipantsReportAdmin)
