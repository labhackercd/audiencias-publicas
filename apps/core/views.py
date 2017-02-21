from django.conf import settings
from django.http import HttpResponse
from django.contrib.sites.models import Site
from apps.core.models import Agenda, Video, Question, Room
from apps.core.utils import encrypt
from django.views.generic import DetailView, ListView
import requests
import json
from datetime import datetime
from django.shortcuts import render, get_object_or_404


def associate_videos(video):
    params = {'part': 'snippet,id',
              'channelId': settings.YOUTUBE_CHANNEL_ID,
              'id': video.videoId,
              'key': settings.YOUTUBE_API_KEY}
    response = requests.get('https://www.googleapis.com/youtube/v3/videos',
                            params=params)
    data = json.loads(response.text)
    tags = data['items'][0]['snippet']['tags']
    for tag in tags:
        if 'IDSessaoReuniao' in tag:
            cod = tag.split(' ')[1]
            try:
                room = Room.objects.get(cod_reunion=cod)
                room.video_id = video.id
                room.save()
            except Room.DoesNotExist:
                pass


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
        associate_videos(video)
    return HttpResponse('<h1>Receive callback</h1>', status=200)


def index(request):
    return render(request, 'index.html', context=dict(
        closed_videos=Room.objects.filter(
            video__closed_date__isnull=False,
            is_visible=True).order_by('-video__published_date')[:5],
        live_videos=Room.objects.filter(
            video__isnull=False,
            video__closed_date__isnull=True,
            is_visible=True).order_by('-video__published_date'),
        agendas=Agenda.objects.filter(
            room__is_visible=True,
            situation__startswith='Convocada',
            session__icontains='Audiência Pública',
            date__gte=datetime.now()).order_by('date'),
    ))


class VideoDetail(DetailView):
    model = Room
    template_name = 'room.html'

    def get_context_data(self, **kwargs):
        context = super(VideoDetail, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['handler'] = encrypt(str(self.request.user.id).rjust(10))
        context['questions'] = sorted(self.object.questions.all(),
                                      key=lambda vote: vote.votes_count,
                                      reverse=True)
        context['answer_time'] = self.request.GET.get('t', None)
        context['domain'] = Site.objects.get_current().domain
        context['domain'] += settings.FORCE_SCRIPT_NAME

        return context


class ClosedVideos(ListView):
    model = Room
    template_name = 'video-list.html'

    def get_queryset(self):
        return Room.objects.filter(
            is_visible=True,
            video__closed_date__isnull=False
        ).order_by('-video__published_date')


class RoomQuestionList(DetailView):
    model = Room
    template_name = 'room_questions_list.html'

    def get_context_data(self, **kwargs):
        context = super(RoomQuestionList, self).get_context_data(**kwargs)
        questions = self.object.questions.all()
        context['no_offset_top'] = 'no-offset-top'
        context['questions'] = sorted(questions,
                                      key=lambda vote: vote.votes_count,
                                      reverse=True)

        return context


class QuestionDetail(DetailView):
    model = Question
    template_name = 'question_meta.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        context['domain'] = Site.objects.get_current().domain
        context['domain'] += settings.FORCE_SCRIPT_NAME

        return context
