from channels import Group
from apps.core.models import Video, Question, UpDownVote
from apps.core.utils import decrypt, encrypt
from apps.core.consumers.utils import get_video, get_data
from django.contrib.auth.models import User
import json
import logging

log = logging.getLogger("chat")


def on_connect(message, pk):
    video = get_video(pk)
    if video is not None:
        Group(video.group_room_questions_name).add(message.reply_channel)
        log.debug('Questions websocket connected.')


def on_disconnect(message, pk):
    try:
        video = Video.objects.get(pk=pk)
        Group(video.group_room_questions_name).discard(message.reply_channel)
        log.debug('Questions websocket disconnected.')
    except (KeyError, Video.DoesNotExist):
        pass
