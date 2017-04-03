# -*- encoding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics, filters, permissions, mixins
from apps.core.models import Message, Question, UpDownVote, Room
from apps.core.serializers import (QuestionSerializer, MessageSerializer,
                                   VoteSerializer, UserSerializer,
                                   RoomSerializer)


class TokenPermission(permissions.BasePermission):
    message = "Admin private token is mandatory to perform this action."

    def has_permission(self, request, view):
        if request.GET.get('api_key') == settings.SECRET_KEY:
            return True
        else:
            return False


class UserListAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (TokenPermission, )


class VoteListAPI(generics.ListAPIView):
    queryset = UpDownVote.objects.all()
    serializer_class = VoteSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter)
    filter_fields = ('user', 'vote')
    search_fields = ('user', 'vote', 'object_pk')
    ordering_fields = ('user', 'vote')


class MessageListAPI(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter)
    filter_fields = ('user', 'room')
    search_fields = ('message',)
    ordering_fields = ('timestamp', 'user', 'room')


class QuestionListAPI(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter)
    filter_fields = ('user', 'room')
    search_fields = ('question',)
    ordering_fields = ('up_votes', 'down_votes', 'timestamp')


class RoomListAPI(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('cod_reunion')


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
