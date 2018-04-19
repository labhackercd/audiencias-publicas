from django.contrib import admin
from apps.core.models import (Message, Question, UpDownVote, Room,
                              RoomAttachment, Video)


class VideoInline(admin.TabularInline):
    model = Video


class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'title_reunion', 'legislative_body_alias',
        'date', 'is_visible')
    list_filter = [
        'reunion_status', 'date']
    search_fields = (
        'title_reunion', 'legislative_body_initials', 'legislative_body_alias',
        'legislative_body', 'location', 'cod_reunion', 'reunion_object')
    inlines = (VideoInline, )


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


class RoomAttachmentAdmin(admin.ModelAdmin):
    list_display = ('room', 'title', 'url')
    list_filter = ['room', 'created']
    search_fields = ['title', 'url']


class VideoAdmin(admin.ModelAdmin):
    list_display = ('room', 'title', 'video_id', 'is_attachment')
    list_filter = ['room', 'created']
    search_fields = ['title', 'video_id']


admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UpDownVote, UpDownVoteAdmin)
admin.site.register(RoomAttachment, RoomAttachmentAdmin)
admin.site.register(Video, VideoAdmin)
