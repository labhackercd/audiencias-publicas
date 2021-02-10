from django.contrib import admin
from apps.reports.models import (NewUsers, VotesReport, RoomsReport,
                                 QuestionsReport)


class NewUsersAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'new_users', 'created')
    list_filter = ['start_date', 'period']


class VotesReportAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'votes', 'created')
    list_filter = ['start_date', 'period']


class RoomsReportAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'rooms', 'created')
    list_filter = ['start_date', 'period']


class QuestionsReportAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'questions', 'created')
    list_filter = ['start_date', 'period']


admin.site.register(NewUsers, NewUsersAdmin)
admin.site.register(VotesReport, VotesReportAdmin)
admin.site.register(RoomsReport, RoomsReportAdmin)
admin.site.register(QuestionsReport, QuestionsReportAdmin)
