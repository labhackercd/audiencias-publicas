# -*- encoding: utf-8 -*-
from django.contrib.auth import get_user_model
from django_filters import FilterSet
from django_filters import rest_framework as django_filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics, filters, mixins
from apps.core.models import Message, Question, UpDownVote, Room
from apps.core.serializers import (QuestionSerializer, MessageSerializer,
                                   VoteSerializer, UserSerializer,
                                   RoomSerializer)


class UserListAPI(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    filter_fields = ('id', )
    search_fields = ('username', 'first_name', 'last_name')


class VoteListAPI(generics.ListAPIView):
    queryset = UpDownVote.objects.all()
    serializer_class = VoteSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter)
    filter_fields = ('user', 'vote')
    search_fields = ('user', 'vote', 'object_pk')
    ordering_fields = ('user', 'vote')


class MessageListAPI(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter)
    filter_fields = ('id', 'room', 'user', 'message')
    search_fields = ('message',)
    ordering_fields = ('timestamp', 'user', 'room')


class QuestionListAPI(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter)
    filter_fields = ('id', 'room', 'user', 'question')
    search_fields = ('question',)
    ordering_fields = ('up_votes', 'down_votes', 'timestamp')


class RoomFilter(FilterSet):
    class Meta:
        model = Room
        fields = {
            'date': ['lt', 'gte'],
            'legislative_body_initials': ['exact'],
            'youtube_id': ['exact'],
            'cod_reunion': ['exact'],
        }


class RoomListAPI(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_class = RoomFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter)
    search_fields = (
        'cod_reunion', 'youtube_id', 'legislative_body_alias',
        'legislative_body_initials', 'reunion_type', 'title_reunion',
        'reunion_object', 'reunion_theme', 'legislative_body',
        'reunion_status', 'location')


class RoomAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        return RoomSerializer

    def get_object(self):
        return Room.objects.get(pk=self.kwargs['pk'])


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'rooms': reverse('room_list_api',
                         request=request, format=format),
        'messages': reverse('message_list_api',
                            request=request, format=format),
        'questions': reverse('question_list_api',
                             request=request, format=format),
        'votes': reverse('vote_list_api',
                         request=request, format=format),
        'users': reverse('user_list_api',
                         request=request, format=format),
    })
