from apps.core.models import Room
import json
import logging

log = logging.getLogger("chat")


def get_room(pk):
    try:
        return Room.objects.get(pk=pk, is_visible=True)
    except ValueError:
        log.debug('Invalid path.')
        return
    except Room.DoesNotExist:
        log.debug('Room does not exists.')
        return


def get_data(message):
    try:
        return json.loads(message['text'])
    except ValueError:
        log.debug("Message isn't json text")
        return
