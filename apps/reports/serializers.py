from rest_framework import serializers
from apps.reports.models import NewUsers, VotesReport
from django.contrib.auth import get_user_model


class NewUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewUsers
        fields = ('start_date', 'end_date', 'period', 'new_users')


class VotesReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = VotesReport
        fields = ('start_date', 'end_date', 'period', 'votes')
