from django.conf import settings
import requests
import json
from apps.core.models import Video, Message, Question
from django.views.generic import TemplateView, DetailView


def receive_callback(request=None):
    params = {'part': 'snippet,id',
              'channelId': settings.YOUTUBE_CHANNEL_ID,
              'q': settings.YOUTUBE_SEARCH_QUERY,
              'type': 'video',
              'eventType': 'live',
              'key': settings.YOUTUBE_API_KEY}
    response = requests.get('https://www.googleapis.com/youtube/v3/search',
                            params=params)
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


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['videos_closed'] = Video.objects.filter(
            closed_date__isnull=False).order_by('-published_date')
        context['videos_live'] = Video.objects.filter(
            closed_date__isnull=True).order_by('-published_date')

        return context


class VideoDetail(DetailView):
    model = Video
    template_name = 'video-room.html'

    def get_context_data(self, **kwargs):
        context = super(VideoDetail, self).get_context_data(**kwargs)
        context['messages'] = Message.objects.filter(video=self.object)
        context['questions'] = Question.objects.filter(video=self.object)
        return context
