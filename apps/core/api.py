from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics, filters
from datetime import datetime
from apps.core.models import Agenda, Message, Question, Video
from apps.core.serializers import (AgendaSerializer, QuestionSerializer,
                                   MessageSerializer, VideoSerializer)


class AgendaListAPI(generics.ListAPIView):
    queryset = Agenda.objects.exclude(date__lt=datetime.now()).order_by('-date')
    serializer_class = AgendaSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('session', 'location', 'situation', 'commission')
    search_fields = ('session', 'location', 'situation', 'commission')
    ordering_fields = ('date', 'commission')


class MessageListAPI(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('user', 'video')
    search_fields = ('message',)
    ordering_fields = ('timestamp', 'user', 'video')


class QuestionListAPI(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('user', 'video')
    search_fields = ('question',)
    ordering_fields = ('up_votes', 'down_votes', 'timestamp')


class VideoListAPI(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('videoId', 'title', 'description', 'slug')
    ordering_fields = ('published_date', 'closed_date')


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'agendas': reverse('agenda_list_api',
                           request=request, format=format),
        'videos': reverse('video_list_api',
                          request=request, format=format),
        'messages': reverse('message_list_api',
                            request=request, format=format),
        'questions': reverse('question_list_api',
                             request=request, format=format),
    })
