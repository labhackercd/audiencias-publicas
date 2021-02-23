# -*- encoding: utf-8 -*-
from django_filters import FilterSet
from django_filters import rest_framework as django_filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets, filters
from apps.reports.models import (NewUsers, VotesReport, RoomsReport,
                                 QuestionsReport, MessagesReport,
                                 ParticipantsReport)
from apps.reports.serializers import (NewUsersSerializer,
                                      VotesReportSerializer,
                                      RoomsReportSerializer,
                                      QuestionsReportSerializer,
                                      MessagesReportSerializer,
                                      ParticipantsReportSerializer)
from django.db.models import Sum


class ModelJSONRenderer(JSONRenderer):
    """
    Add "objects" and "sum_total_results" in Json
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = {'objects': data,
                'sum_total_results': renderer_context['sum_total_results']}
        return super(ModelJSONRenderer, self).render(data, accepted_media_type,
                                                     renderer_context)


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
        filters.OrderingFilter
    )
    ordering_fields = '__all__'
    renderer_classes = (ModelJSONRenderer, )

    def get_queryset(self):
        queryset = self.queryset

        sum_total_results = queryset.aggregate(
            Sum('new_users'))['new_users__sum']

        self.sum_total_results = sum_total_results if sum_total_results else 0

        return queryset

    def get_renderer_context(self):
        """
        Returns a dict that is passed through to Renderer.render(),
        as the `renderer_context` keyword argument.
        """
        return {
            'view': self,
            'args': getattr(self, 'args', ()),
            'kwargs': getattr(self, 'kwargs', {}),
            'request': getattr(self, 'request', None),
            'sum_total_results': self.sum_total_results,
        }


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
        filters.OrderingFilter
    )
    ordering_fields = '__all__'
    renderer_classes = (ModelJSONRenderer, )

    def get_queryset(self):
        queryset = self.queryset

        sum_total_results = queryset.aggregate(
            Sum('votes'))['votes__sum']

        self.sum_total_results = sum_total_results if sum_total_results else 0

        return queryset

    def get_renderer_context(self):
        """
        Returns a dict that is passed through to Renderer.render(),
        as the `renderer_context` keyword argument.
        """
        return {
            'view': self,
            'args': getattr(self, 'args', ()),
            'kwargs': getattr(self, 'kwargs', {}),
            'request': getattr(self, 'request', None),
            'sum_total_results': self.sum_total_results,
        }


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
        filters.OrderingFilter
    )
    ordering_fields = '__all__'
    renderer_classes = (ModelJSONRenderer, )

    def get_queryset(self):
        queryset = self.queryset

        sum_total_results = queryset.aggregate(
            Sum('rooms'))['rooms__sum']

        self.sum_total_results = sum_total_results if sum_total_results else 0

        return queryset

    def get_renderer_context(self):
        """
        Returns a dict that is passed through to Renderer.render(),
        as the `renderer_context` keyword argument.
        """
        return {
            'view': self,
            'args': getattr(self, 'args', ()),
            'kwargs': getattr(self, 'kwargs', {}),
            'request': getattr(self, 'request', None),
            'sum_total_results': self.sum_total_results,
        }



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
        filters.OrderingFilter
    )
    ordering_fields = '__all__'
    renderer_classes = (ModelJSONRenderer, )

    def get_queryset(self):
        queryset = self.queryset

        sum_total_results = queryset.aggregate(
            Sum('questions'))['questions__sum']

        self.sum_total_results = sum_total_results if sum_total_results else 0

        return queryset

    def get_renderer_context(self):
        """
        Returns a dict that is passed through to Renderer.render(),
        as the `renderer_context` keyword argument.
        """
        return {
            'view': self,
            'args': getattr(self, 'args', ()),
            'kwargs': getattr(self, 'kwargs', {}),
            'request': getattr(self, 'request', None),
            'sum_total_results': self.sum_total_results,
        }


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
        filters.OrderingFilter
    )
    ordering_fields = '__all__'
    renderer_classes = (ModelJSONRenderer, )

    def get_queryset(self):
        queryset = self.queryset

        sum_total_results = queryset.aggregate(
            Sum('messages'))['messages__sum']

        self.sum_total_results = sum_total_results if sum_total_results else 0

        return queryset

    def get_renderer_context(self):
        """
        Returns a dict that is passed through to Renderer.render(),
        as the `renderer_context` keyword argument.
        """
        return {
            'view': self,
            'args': getattr(self, 'args', ()),
            'kwargs': getattr(self, 'kwargs', {}),
            'request': getattr(self, 'request', None),
            'sum_total_results': self.sum_total_results,
        }


class ParticipantsReportFilter(FilterSet):
    class Meta:
        model = ParticipantsReport
        fields = {
            'start_date': ['lt', 'lte', 'gt', 'gte'],
            'end_date': ['lt', 'lte', 'gt', 'gte'],
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
    renderer_classes = (ModelJSONRenderer, )

    def get_queryset(self):
        queryset = self.queryset

        sum_total_results = queryset.aggregate(
            Sum('participants'))['participants__sum']

        self.sum_total_results = sum_total_results if sum_total_results else 0

        return queryset

    def get_renderer_context(self):
        """
        Returns a dict that is passed through to Renderer.render(),
        as the `renderer_context` keyword argument.
        """
        return {
            'view': self,
            'args': getattr(self, 'args', ()),
            'kwargs': getattr(self, 'kwargs', {}),
            'request': getattr(self, 'request', None),
            'sum_total_results': self.sum_total_results,
        }


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
    })
