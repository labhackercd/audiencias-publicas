from rest_framework import serializers
from apps.reports.models import (NewUsers, VotesReport, RoomsReport,
                                 QuestionsReport, MessagesReport,
                                 ParticipantsReport)
from apps.core.models import Room


class NewUsersSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()

    def get_month(self, obj):
        return obj.start_date.month

    def get_year(self, obj):
        return obj.start_date.year

    class Meta:
        model = NewUsers
        fields = ('start_date', 'end_date', 'period', 'new_users', 'month',
                  'year')


class VotesReportSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()

    def get_month(self, obj):
        return obj.start_date.month

    def get_year(self, obj):
        return obj.start_date.year

    class Meta:
        model = VotesReport
        fields = ('start_date', 'end_date', 'period', 'votes', 'month',
                  'year')


class RoomsReportSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()

    def get_month(self, obj):
        return obj.start_date.month

    def get_year(self, obj):
        return obj.start_date.year

    class Meta:
        model = RoomsReport
        fields = ('start_date', 'end_date', 'period', 'rooms', 'month',
                  'year')


class QuestionsReportSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()

    def get_month(self, obj):
        return obj.start_date.month

    def get_year(self, obj):
        return obj.start_date.year

    class Meta:
        model = QuestionsReport
        fields = ('start_date', 'end_date', 'period', 'questions', 'month',
                  'year')


class MessagesReportSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()

    def get_month(self, obj):
        return obj.start_date.month

    def get_year(self, obj):
        return obj.start_date.year

    class Meta:
        model = MessagesReport
        fields = ('start_date', 'end_date', 'period', 'messages', 'month',
                  'year')


class ParticipantsReportSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()

    def get_month(self, obj):
        return obj.start_date.month

    def get_year(self, obj):
        return obj.start_date.year

    class Meta:
        model = ParticipantsReport
        fields = ('start_date', 'end_date', 'period', 'participants', 'month',
                  'year')


class RoomRankingSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%d")
    messages_count = serializers.ReadOnlyField()
    questions_count = serializers.ReadOnlyField()
    votes_count = serializers.ReadOnlyField()
    participants_count = serializers.ReadOnlyField()

    class Meta:
        model = Room
        fields = ('title_reunion', 'reunion_theme',
                  'legislative_body_initials', 'date',
                  'messages_count', 'questions_count', 'votes_count',
                  'participants_count', 'get_absolute_url')
