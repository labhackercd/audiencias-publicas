import json
import logging
import re
from channels import Group
from apps.core.models import Room, Message
from apps.core.utils import decrypt
from apps.core.consumers.utils import get_room, get_data
from django.contrib.auth.models import User
from django.conf import settings
from channels_presence.models import Room as RoomPresence, Presence
from channels.auth import channel_session_user
from channels_presence.decorators import touch_presence

log = logging.getLogger("chat")


@channel_session_user
def on_connect(message, pk):
    message.reply_channel.send({
        'accept': True
    })
    room = get_room(pk)
    if room is not None:
        room_presence = RoomPresence.objects.add(room.group_questions_name,
                                                 message.reply_channel.name,
                                                 message.user)
        room_presence.prune_presences(age_in_seconds=10)
        room.online_users = room_presence.get_anonymous_count()
        room.views += 1
        if room.online_users > room.max_online_users:
            room.max_online_users = room.online_users
        room.save()
        Group(room.group_chat_name).add(message.reply_channel)
        log.debug('Chat websocket connected.')


@touch_presence
def on_receive(message, pk):
    room = get_room(pk)
    data = get_data(message)

    if message.content('text') == '"heartbeat"':
        Presence.objects.touch(message.reply_channel.name)

    if set(data.keys()) != set(('handler', 'message')):
        log.debug("Message unexpected format data")
        return
    else:
        log.debug('Chat message is ok.')

    black_list = settings.WORDS_BLACK_LIST
    word_list = re.sub("[^\w]", " ", data['message'].lower()).split()
    censured_words = list(set(black_list) & set(word_list))

    message = data['message']

    if message.strip():
        if censured_words:
            for word in censured_words:
                message = re.sub(word, '♥', message, flags=re.IGNORECASE)

        user = User.objects.get(id=decrypt(data['handler']))
        message = Message.objects.create(room=room, user=user,
                                         message=message)
        Group(room.group_chat_name).send(
            {'text': json.dumps({"hmtl": message.html_body()})}
        )


def on_disconnect(message, pk):
    try:
        room = Room.objects.get(pk=pk)
        RoomPresence.objects.remove(room.group_questions_name, message.reply_channel.name)
        Group(room.group_chat_name).discard(message.reply_channel)
        log.debug('Chat websocket disconnected.')
    except (KeyError, Room.DoesNotExist):
        pass
