# -*- encoding: utf-8 -*-
from django.contrib.auth import get_user_model
from django_filters import FilterSet
from django_filters import rest_framework as django_filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import filters, viewsets
from apps.core.models import Message, Question, UpDownVote, Room
from apps.core.serializers import (QuestionSerializer, MessageSerializer,
                                   VoteSerializer, UserSerializer,
                                   RoomSerializer)


class UserFilter(FilterSet):
    class Meta:
        model = get_user_model()
        fields = {
            'date_joined': ['lt', 'lte', 'gt', 'gte'],
            'last_login': ['lt', 'lte', 'gt', 'gte'],
            'id': ['exact'],
            'username': ['exact', 'contains'],
            'first_name': ['exact', 'contains'],
            'last_name': ['exact', 'contains'],
        }


class UserViewSet(viewsets.ModelViewSet):
    allowed_methods = ['get', 'put', 'delete']
    lookup_field = 'username'
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
    )
    search_fields = ('username', 'first_name', 'last_name')


class VoteViewSet(viewsets.ModelViewSet):
    allowed_methods = ['get']
    queryset = UpDownVote.objects.all()
    serializer_class = VoteSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter)
    filter_fields = ('user', 'vote', 'user__username')
    search_fields = ('user', 'vote', 'object_pk')
    ordering_fields = ('user', 'vote')


class MessageFilter(FilterSet):
    class Meta:
        model = Message
        fields = {
            'created': ['lt', 'lte', 'gt', 'gte'],
            'modified': ['lt', 'lte', 'gt', 'gte'],
            'id': ['exact'],
            'room__id': ['exact'],
            'room__cod_reunion': ['exact'],
            'room__legislative_body_initials': ['exact'],
            'room__title_reunion': ['exact', 'contains'],
            'user__id': ['exact'],
            'user__username': ['exact', 'contains'],
            'user__first_name': ['exact', 'contains'],
            'user__last_name': ['exact', 'contains'],
            'message': ['exact', 'contains'],
        }


class MessageViewSet(viewsets.ModelViewSet):
    allowed_methods = ['get']
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_class = MessageFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter)
    search_fields = ('message',)
    ordering_fields = ('created', 'modified', 'user', 'room')


class QuestionFilter(FilterSet):
    class Meta:
        model = Question
        fields = {
            'created': ['lt', 'lte', 'gt', 'gte'],
            'modified': ['lt', 'lte', 'gt', 'gte'],
            'id': ['exact'],
            'room__id': ['exact'],
            'room__cod_reunion': ['exact'],
            'room__legislative_body_initials': ['exact'],
            'room__title_reunion': ['exact', 'contains'],
            'user__id': ['exact'],
            'user__username': ['exact', 'contains'],
            'user__first_name': ['exact', 'contains'],
            'user__last_name': ['exact', 'contains'],
            'question': ['exact', 'contains'],
        }


class QuestionViewSet(viewsets.ModelViewSet):
    allowed_methods = ['get']
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_class = QuestionFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter)
    search_fields = ('question',)
    ordering_fields = ('created', 'modified')


class RoomFilter(FilterSet):
    class Meta:
        model = Room
        fields = {
            'date': ['lt', 'lte', 'gt', 'gte', 'year', 'month', 'day'],
            'legislative_body_initials': ['exact'],
            'cod_reunion': ['exact'],
            'is_visible': ['exact'],
            'youtube_status': ['exact'],
        }


class RoomViewSet(viewsets.ModelViewSet):
    allowed_methods = ['get']
    queryset = Room.objects.filter(is_active=True)
    serializer_class = RoomSerializer
    filter_class = RoomFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter)
    search_fields = (
        'cod_reunion', 'legislative_body_initials', 'reunion_type',
        'title_reunion', 'reunion_object', 'reunion_theme', 'legislative_body',
        'location')
    ordering_fields = '__all__'


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'rooms': reverse('room-list',
                         request=request, format=format),
        'messages': reverse('message-list',
                            request=request, format=format),
        'questions': reverse('question-list',
                             request=request, format=format),
        'votes': reverse('updownvote-list',
                         request=request, format=format),
        'users': reverse('user-list',
                         request=request, format=format),
    })
