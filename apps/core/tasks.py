from django_q.models import Schedule
from django.conf import settings
from django.utils import timezone
from .models import Video
import requests
import json


def close_room(video_id):
    params = {'part': 'snippet,id',
              'channelId': settings.YOUTUBE_CHANNEL_ID,
              'q': settings.YOUTUBE_SEARCH_QUERY,
              'type': 'video',
              'eventType': 'completed',
              'order': 'date',
              'maxResults': 50,
              'key': settings.YOUTUBE_API_KEY}
    response = requests.get('https://www.googleapis.com/youtube/v3/search',
                            params=params)
    data = json.loads(response.text)
    for item in data['items']:
        if video_id == item['id']['videoId']:
            video = Video.objects.get(videoId=video_id)
            video.closed_date = timezone.now()
            video.save()
            Schedule.objects.get(name=video_id).delete()
