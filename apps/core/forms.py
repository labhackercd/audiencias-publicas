from django import forms
from apps.core.models import RoomAttachment


class RoomAttachmentForm(forms.ModelForm):
    required = ('url', 'title')

    class Meta:
        fields = ('url', 'title')
        model = RoomAttachment
