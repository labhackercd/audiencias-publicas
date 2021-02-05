from rest_framework import serializers
from apps.reports.models import NewUsers
from django.contrib.auth import get_user_model


class NewUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewUsers
        fields = ('start_date', 'end_date', 'period', 'new_users')
