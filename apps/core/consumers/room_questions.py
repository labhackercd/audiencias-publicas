from channels import Group
from apps.core.models import Room
from apps.core.consumers.utils import get_room
import logging

log = logging.getLogger("chat")


def on_connect(message, pk):
    message.reply_channel.send({
        'accept': True
    })
    room = get_room(pk)
    if room is not None:
        Group(room.group_room_questions_name).add(message.reply_channel)
        log.debug('Questions websocket connected.')


def on_disconnect(message, pk):
    try:
        room = Room.objects.get(pk=pk)
        Group(room.group_room_questions_name).discard(message.reply_channel)
        log.debug('Questions websocket disconnected.')
    except (KeyError, Room.DoesNotExist):
        pass
