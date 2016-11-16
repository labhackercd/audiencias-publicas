from django.conf import settings
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from apps.core.models import Video, Agenda
from apps.core.utils import encrypt
from django.views.generic import DetailView
import requests
import json
from datetime import datetime
from django.shortcuts import render


def receive_callback(request=None):
    params = {'part': 'snippet,id',
              'channelId': settings.YOUTUBE_CHANNEL_ID,
              'q': settings.YOUTUBE_SEARCH_QUERY,
              'type': 'video',
              'eventType': 'live',
              'order': 'date',
              'maxResults': 50,
              'key': settings.YOUTUBE_API_KEY}
    response = requests.get('https://www.googleapis.com/youtube/v3/search',
                            params=params)
    data = json.loads(response.text)
    for item in data['items']:
        video, created = Video.objects.get_or_create(
            videoId=item['id']['videoId'])
        video.title = item['snippet']['title']
        video.description = item['snippet']['description']
        video.thumb_default = item['snippet']['thumbnails']['default']['url']
        video.thumb_medium = item['snippet']['thumbnails']['medium']['url']
        video.thumb_high = item['snippet']['thumbnails']['high']['url']
        video.save()
    return HttpResponse('<h1>Receive callback</h1>', status=200)


def index(request):
    return render(request, 'index.html', context=dict(
        closed_videos=Video.objects.filter(
            closed_date__isnull=False).order_by('-published_date')[:5],
        live_videos=Video.objects.filter(
            closed_date__isnull=True).order_by('-published_date'),
        agendas=Agenda.objects.filter(
            situation__startswith='Convocada',
            session__icontains='Audiência Pública',
            date__gte=datetime.now()).order_by('date'),
        no_offset_top='no-offset-top',
        hidden_nav='navigation--hidden',
    ))


class VideoDetail(DetailView):
    model = Video
    template_name = 'room.html'

    def get_context_data(self, **kwargs):
        context = super(VideoDetail, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['handler'] = encrypt(str(self.request.user.id).rjust(10))
        context['questions'] = sorted(self.object.questions.all(),
                                      key=lambda vote: vote.votes_count,
                                      reverse=True)

        return context


def notification(subject, html, email_list):
    mail = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER,
                                  email_list)
    mail.attach_alternative(html, 'text/html')
    mail.send()
