import json
import logging
from channels import Group
from apps.core.models import Video, Message
from apps.core.utils import decrypt
from apps.core.consumers.utils import get_video, get_data
from django.contrib.auth.models import User

log = logging.getLogger("chat")


def on_connect(message, pk):
    video = get_video(pk)
    if video is not None:
        Group(video.group_chat_name).add(message.reply_channel)
        log.debug('Chat websocket connected.')


def on_receive(message, pk):
    video = get_video(pk)
    data = get_data(message)

    if set(data.keys()) != set(('handler', 'message')):
        log.debug("Message unexpected format data")
        return
    else:
        log.debug('Chat message is ok.')

    user = User.objects.get(id=decrypt(data['handler']))
    message = Message.objects.create(video=video, user=user,
                                     message=data['message'])
    Group(video.group_chat_name).send(
        {'text': json.dumps({"hmtl": message.html_body()})}
    )


def on_disconnect(message, pk):
    try:
        video = Video.objects.get(pk=pk)
        Group(video.group_chat_name).discard(message.reply_channel)
        log.debug('Chat websocket disconnected.')
    except (KeyError, Video.DoesNotExist):
        pass
