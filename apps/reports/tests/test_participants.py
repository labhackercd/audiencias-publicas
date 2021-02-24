import pytest
from mixer.backend.django import mixer
from apps.reports.models import ParticipantsReport
from django.db import IntegrityError
from apps.core.models import Message
from apps.reports.tasks import (create_participants_object,
                                get_participants_daily,
                                get_participants_monthly,
                                get_participants_yearly)
from datetime import date, timedelta
from django.urls import reverse
import json
from rest_framework.test import APIClient
import calendar


class TestParticipantsReport():
    @pytest.mark.django_db
    def test_participants_create(self):
        participants = mixer.blend(ParticipantsReport)
        assert ParticipantsReport.objects.count() == 1
        assert participants.__str__() == ('{} - {}').format(
            participants.start_date.strftime("%d/%m/%Y"), participants.period)

    @pytest.mark.django_db
    def test_participants_integrity_error(self):
        content = mixer.blend(ParticipantsReport)
        with pytest.raises(IntegrityError) as excinfo:
            mixer.blend(ParticipantsReport,
                        period=content.period,
                        start_date=content.start_date)
        assert 'UNIQUE constraint failed' in str(
            excinfo.value)
        ## PostgreSQL message error
        # assert 'duplicate key value violates unique constraint' in str(
        #     excinfo.value)

    def test_create_participants_daily(self):
        data_daily = ['2020-11-23', 10]
        participants_object = create_participants_object(data_daily, 'daily')

        assert participants_object.period == 'daily'
        assert participants_object.start_date == '2020-11-23'
        assert participants_object.end_date == '2020-11-23'
        assert participants_object.participants == 10

    def test_create_participants_monthly(self):
        data_monthly = {
            'month': date(2020, 1, 1),
            'total_participants': 10
        }

        participants_object = create_participants_object(data_monthly, 'monthly')

        assert participants_object.period == 'monthly'
        assert participants_object.start_date == date(2020, 1, 1)
        assert participants_object.end_date == date(2020, 1, 31)
        assert participants_object.participants == 10

    def test_create_participants_yearly(self):
        data_yearly = {
            'year': date(2019, 1, 1),
            'total_participants': 10
        }

        participants_object = create_participants_object(data_yearly, 'yearly')

        assert participants_object.period == 'yearly'
        assert participants_object.start_date == date(2019, 1, 1)
        assert participants_object.end_date == date(2019, 12, 31)
        assert participants_object.participants == 10

    @pytest.mark.django_db
    def test_get_participants_daily_without_args(self):
        today = date.today()
        mixer.blend(Message)

        get_participants_daily.apply()

        daily_data = ParticipantsReport.objects.filter(
            period='daily').first()

        assert daily_data.start_date == today
        assert daily_data.end_date == today
        assert daily_data.period == 'daily'
        assert daily_data.participants == 1

    @pytest.mark.django_db
    def test_get_participants_monthly_without_args(self):
        today = date.today()
        mixer.blend(ParticipantsReport, period='daily', participants=10,
                    start_date=today, end_date=today)

        get_participants_monthly.apply()

        monthly_data = ParticipantsReport.objects.filter(
            period='monthly').first()

        last_day = calendar.monthrange(today.year,
                                       today.month)[1]
        assert monthly_data.start_date == today.replace(day=1)
        assert monthly_data.end_date == today.replace(day=last_day)
        assert monthly_data.period == 'monthly'
        assert monthly_data.participants == 10

    @pytest.mark.django_db
    def test_get_participants_yearly_without_args(self):
        today = date.today()
        last_day_month = calendar.monthrange(today.year, today.month)[1]
        mixer.blend(ParticipantsReport, period='monthly', participants=10,
                    start_date=today.replace(day=1),
                    end_date=today.replace(day=last_day_month))

        get_participants_yearly.apply()

        yearly_data = ParticipantsReport.objects.filter(
            period='yearly').first()

        assert yearly_data.start_date == today.replace(day=1, month=1)
        assert yearly_data.end_date == today.replace(day=31, month=12)
        assert yearly_data.period == 'yearly'
        assert yearly_data.participants == 10

    @pytest.mark.django_db
    def test_participants_api_url(api_client):
        mixer.cycle(5).blend(ParticipantsReport)
        url = reverse('participantsreport-list')
        client = APIClient()
        response = client.get(url)
        request = json.loads(response.content)

        assert response.status_code == 200
        assert request['objects']['count'] == 5
