from django.core.management.base import BaseCommand
from django.conf import settings
import requests
import json
from apps.core.models import Video


class Command(BaseCommand):
    def handle(self, *args, **options):
        params = {'part': 'snippet,id',
                  'channelId': 'UC-ZkSRh-7UEuwXJQ9UMCFJA',
                  'q': 'audiencias publicas',
                  'type': 'video',
                  'eventType': 'live',
                  'key': settings.YOUTUBE_API_KEY}
        response = requests.get('https://www.googleapis.com/youtube/v3/search', params=params)
        data = json.loads(response.text)
        for item in data['items']:
            video = Video()
            video.videoId = item['id']['videoId']
            video.title = item['snippet']['title']
            video.description = item['snippet']['description']
            video.thumb_default = item['snippet']['thumbnails']['default']['url']
            video.thumb_medium = item['snippet']['thumbnails']['medium']['url']
            video.thumb_high = item['snippet']['thumbnails']['high']['url']
            video.save()
