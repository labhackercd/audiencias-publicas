from django.contrib import admin
from apps.core.models import (Message, Question, UpDownVote, Room,
                              RoomAttachment, Video)


class VideoInline(admin.TabularInline):
    model = Video


class RoomAdmin(admin.ModelAdmin):
    list_display = ('reunion_type', 'title_reunion', 'date', 'is_visible',
                    'is_active')
    list_filter = ['youtube_status', 'date']
    search_fields = (
        'title_reunion', 'legislative_body_initials', 'legislative_body',
        'location', 'cod_reunion', 'reunion_object')
    inlines = (VideoInline, )


class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'message', 'created')
    list_filter = ['created']
    search_fields = ['message', 'user', 'room']
    raw_id_fields = ('user', 'room')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'question', 'created')
    list_filter = ['created']
    search_fields = ['question', 'user', 'room']
    raw_id_fields = ('room', 'user', 'video')


class UpDownVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'created')
    list_filter = ['created']
    search_fields = ['user', 'question']
    raw_id_fields = ('user', 'question')


class RoomAttachmentAdmin(admin.ModelAdmin):
    list_display = ('room', 'title', 'url')
    list_filter = ['created']
    search_fields = ['title', 'url', 'room']
    raw_id_fields = ('room', )


class VideoAdmin(admin.ModelAdmin):
    list_display = ('room', 'title', 'video_id', 'is_attachment')
    list_filter = ['created', 'is_attachment']
    search_fields = ['title', 'video_id', 'room']
    raw_id_fields = ('room', )


admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UpDownVote, UpDownVoteAdmin)
admin.site.register(RoomAttachment, RoomAttachmentAdmin)
admin.site.register(Video, VideoAdmin)
