# -*- encoding: utf-8 -*-
from django_filters import FilterSet
from django_filters import rest_framework as django_filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from apps.reports.models import (NewUsers, VotesReport, RoomsReport,
                                 QuestionsReport, MessagesReport)
from apps.reports.serializers import (NewUsersSerializer,
                                      VotesReportSerializer,
                                      RoomsReportSerializer,
                                      QuestionsReportSerializer,
                                      MessagesReportSerializer)


class NewUsersFilter(FilterSet):
    class Meta:
        model = NewUsers
        fields = {
            'start_date': ['lt', 'lte', 'gt', 'gte'],
            'end_date': ['lt', 'lte', 'gt', 'gte'],
            'period': ['exact'],
        }


class NewUsersViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_methods = ['get']
    queryset = NewUsers.objects.all()
    serializer_class = NewUsersSerializer
    filter_class = NewUsersFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
    )


class VotesReportFilter(FilterSet):
    class Meta:
        model = VotesReport
        fields = {
            'start_date': ['lt', 'lte', 'gt', 'gte'],
            'end_date': ['lt', 'lte', 'gt', 'gte'],
            'period': ['exact'],
        }


class VotesReportViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_methods = ['get']
    queryset = VotesReport.objects.all()
    serializer_class = VotesReportSerializer
    filter_class = VotesReportFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
    )


class RoomsReportFilter(FilterSet):
    class Meta:
        model = RoomsReport
        fields = {
            'start_date': ['lt', 'lte', 'gt', 'gte'],
            'end_date': ['lt', 'lte', 'gt', 'gte'],
            'period': ['exact'],
        }


class RoomsReportViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_methods = ['get']
    queryset = RoomsReport.objects.all()
    serializer_class = RoomsReportSerializer
    filter_class = RoomsReportFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
    )


class QuestionsReportFilter(FilterSet):
    class Meta:
        model = QuestionsReport
        fields = {
            'start_date': ['lt', 'lte', 'gt', 'gte'],
            'end_date': ['lt', 'lte', 'gt', 'gte'],
            'period': ['exact'],
        }


class QuestionsReportViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_methods = ['get']
    queryset = QuestionsReport.objects.all()
    serializer_class = QuestionsReportSerializer
    filter_class = QuestionsReportFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
    )


class MessagesReportFilter(FilterSet):
    class Meta:
        model = MessagesReport
        fields = {
            'start_date': ['lt', 'lte', 'gt', 'gte'],
            'end_date': ['lt', 'lte', 'gt', 'gte'],
            'period': ['exact'],
        }


class MessagesReportViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_methods = ['get']
    queryset = MessagesReport.objects.all()
    serializer_class = MessagesReportSerializer
    filter_class = MessagesReportFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
    )


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
    })
