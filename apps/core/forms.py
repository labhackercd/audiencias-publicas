from django import forms
from apps.core.models import RoomAttachment, Video


class RoomAttachmentForm(forms.ModelForm):
    required = ('url', 'title')

    class Meta:
        fields = ('url', 'title')
        model = RoomAttachment


class VideoForm(forms.ModelForm):
    required = ('video_id', 'title')

    class Meta:
        fields = ('video_id', 'title')
        model = Video
