from django.contrib import admin
from apps.reports.models import NewUsers, VotesReport


class NewUsersAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'new_users', 'created')
    list_filter = ['start_date', 'period']


class VotesReportAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'votes', 'created')
    list_filter = ['start_date', 'period']


admin.site.register(NewUsers, NewUsersAdmin)
admin.site.register(VotesReport, VotesReportAdmin)