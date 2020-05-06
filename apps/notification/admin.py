from django.contrib import admin
from apps.notification.models import ParticipantNotification


class ParticipantNotificationAdmin(admin.ModelAdmin):
    list_display = (
        'room', 'created')
    list_filter = ['created']
    search_fields = (
        'room__title_reunion', 'room__legislative_body_initials',
        'room__legislative_body',
        'room__location', 'room__cod_reunion', 'room__reunion_object',
        'emails', 'content')


admin.site.register(ParticipantNotification, ParticipantNotificationAdmin)
