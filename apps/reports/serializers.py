from rest_framework import serializers
from apps.reports.models import (NewUsers, VotesReport, RoomsReport,
                                 QuestionsReport, MessagesReport)


class NewUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewUsers
        fields = ('start_date', 'end_date', 'period', 'new_users')


class VotesReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = VotesReport
        fields = ('start_date', 'end_date', 'period', 'votes')


class RoomsReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomsReport
        fields = ('start_date', 'end_date', 'period', 'rooms')


class QuestionsReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionsReport
        fields = ('start_date', 'end_date', 'period', 'questions')


class MessagesReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessagesReport
        fields = ('start_date', 'end_date', 'period', 'messages')
