import json
import logging
from channels import Group
from apps.core.models import Video, Message
from django.contrib.auth.models import User

log = logging.getLogger("chat")


def connect_room(message, pk):
    try:
        video = Video.objects.get(pk=pk)
    except ValueError:
        log.debug('invalid ws path=%s', message['path'])
        return
    except Video.DoesNotExist:
        log.debug('ws video does not exist pk=%s', pk)
        return

    log.debug('chat connect video=%s client=%s:%s', video.pk, message['client'][0], message['client'][1])

    Group(video.group_name).add(message.reply_channel)


def receive_room(message, pk):
    try:
        video = Video.objects.get(pk=pk)
    except KeyError:
        log.debug('no video in channel_session')
        return
    except Video.DoesNotExist:
        log.debug('recieved message, buy room does not exist video=%s', pk)
        return
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", message['text'])
        return
    if set(data.keys()) != set(('user', 'message')):
        log.debug("ws message unexpected format data=%s", data)
        return

    if data:
        log.debug('chat message video=%s user=%s message=%s', video.pk, data['user'], data['message'])
        user = User.objects.get(id=data['user'])
        m = Message.objects.create(video=video, user=user, message=data['message'])
        Group(video.group_name).send(
            {'text': json.dumps({"user": m.user.username,
                                 "message": m.message,
                                 "created": m.created.strftime("%a %d %b %Y %H:%M")})})


def disconnect_room(message, pk):
    try:
        video = Video.objects.get(pk=pk)
        Group(video.group_name).discard(message.reply_channel)
    except (KeyError, Video.DoesNotExist):
        pass
