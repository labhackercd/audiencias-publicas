from apps.core.models import Video
import json
import logging

log = logging.getLogger("chat")


def get_video(pk):
    try:
        return Video.objects.get(pk=pk)
    except ValueError:
        log.debug('Invalid path.')
        return
    except Video.DoesNotExist:
        log.debug('Video does not exists.')
        return


def get_data(message):
    try:
        return json.loads(message['text'])
    except ValueError:
        log.debug("Message isn't json text")
        return
