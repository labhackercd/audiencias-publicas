# -*- encoding: utf-8 -*-
from django_filters import FilterSet
from django_filters import rest_framework as django_filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from apps.reports.models import (NewUsers, VotesReport, RoomsReport,
                                 QuestionsReport, MessagesReport,
                                 ParticipantsReport)
from apps.reports.serializers import (NewUsersSerializer,
                                      VotesReportSerializer,
                                      RoomsReportSerializer,
                                      QuestionsReportSerializer,
                                      MessagesReportSerializer,
                                      ParticipantsReportSerializer,
                                      RoomRankingSerializer)
from apps.core.models import Room
from django.db.models import Sum
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class NewUsersFilter(FilterSet):
    class Meta:
        model = NewUsers
        fields = {
            'start_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'end_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'period': ['exact'],
        }


class NewUsersViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_methods = ['get']
    queryset = NewUsers.objects.all()
    serializer_class = NewUsersSerializer
    filter_class = NewUsersFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter
    )
    ordering_fields = '__all__'

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['sum_total_results'] = sum([data.get('new_users', 0)
            for data in response.data['results']])
        return response


class VotesReportFilter(FilterSet):
    class Meta:
        model = VotesReport
        fields = {
            'start_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'end_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'period': ['exact'],
        }


class VotesReportViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_methods = ['get']
    queryset = VotesReport.objects.all()
    serializer_class = VotesReportSerializer
    filter_class = VotesReportFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter
    )
    ordering_fields = '__all__'

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['sum_total_results'] = sum([data.get('votes', 0)
            for data in response.data['results']])
        return response


class RoomsReportFilter(FilterSet):
    class Meta:
        model = RoomsReport
        fields = {
            'start_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'end_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'period': ['exact'],
        }


class RoomsReportViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_methods = ['get']
    queryset = RoomsReport.objects.all()
    serializer_class = RoomsReportSerializer
    filter_class = RoomsReportFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter
    )
    ordering_fields = '__all__'

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['sum_total_results'] = sum([data.get('rooms', 0)
            for data in response.data['results']])
        return response


class QuestionsReportFilter(FilterSet):
    class Meta:
        model = QuestionsReport
        fields = {
            'start_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'end_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'period': ['exact'],
        }


class QuestionsReportViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_methods = ['get']
    queryset = QuestionsReport.objects.all()
    serializer_class = QuestionsReportSerializer
    filter_class = QuestionsReportFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter
    )
    ordering_fields = '__all__'

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['sum_total_results'] = sum([data.get('questions', 0)
            for data in response.data['results']])
        return response


class MessagesReportFilter(FilterSet):
    class Meta:
        model = MessagesReport
        fields = {
            'start_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'end_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'period': ['exact'],
        }


class MessagesReportViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_methods = ['get']
    queryset = MessagesReport.objects.all()
    serializer_class = MessagesReportSerializer
    filter_class = MessagesReportFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter
    )
    ordering_fields = '__all__'

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['sum_total_results'] = sum([data.get('messages', 0)
            for data in response.data['results']])
        return response


class ParticipantsReportFilter(FilterSet):
    class Meta:
        model = ParticipantsReport
        fields = {
            'start_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'end_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'period': ['exact'],
        }


class ParticipantsReportViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_methods = ['get']
    queryset = ParticipantsReport.objects.all()
    serializer_class = ParticipantsReportSerializer
    filter_class = ParticipantsReportFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter
    )
    ordering_fields = '__all__'

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['sum_total_results'] = sum([data.get('participants', 0)
            for data in response.data['results']])
        return response


class RoomRankingFilter(FilterSet):
    class Meta:
        model = Room
        fields = {
            'date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'legislative_body_initials': ['exact'],
        }


class RoomRankingViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_methods = ['get']
    queryset = Room.objects.filter(is_active=True, is_visible=True)
    serializer_class = RoomRankingSerializer
    pagination_class = LimitOffsetPagination
    filter_class = RoomRankingFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    )
    search_fields = (
        'legislative_body_initials', 'legislative_body', 'reunion_type',
        'title_reunion', 'reunion_object', 'reunion_theme')
    ordering_fields = ('date', 'messages_count', 'questions_count',
                       'votes_count', 'participants_count')

    @method_decorator(cache_page(60 * 60 * 2)) # 2 hours
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@api_view(['GET'])
def api_reports_root(request, format=None):
    return Response({
        'newusers': reverse('newusers-list',
                            request=request, format=format),
        'votes': reverse('votesreport-list',
                         request=request, format=format),
        'rooms': reverse('roomsreport-list',
                         request=request, format=format),
        'questions': reverse('questionsreport-list',
                             request=request, format=format),
        'messages': reverse('messagesreport-list',
                            request=request, format=format),
        'participants': reverse('participantsreport-list',
                                request=request, format=format),
        'ranking': reverse('ranking-list',
                           request=request, format=format),
    })
