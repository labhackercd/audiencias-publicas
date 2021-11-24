from apps.core.models import Room
import json
import logging

log = logging.getLogger('ws-logger')


def get_room(pk):
    try:
        return Room.objects.get(pk=pk, is_active=True)
    except ValueError:
        log.info('Invalid path.')
        return
    except Room.DoesNotExist:
        log.info('Room does not exists.')
        return


def get_data(json_text):
    try:
        return json.loads(json_text)
    except ValueError:
        log.info("Message isn't json text")
        return
