import pytest
from mixer.backend.django import mixer
from apps.reports.models import MessagesReport
from apps.core.models import Message, Room
from django.db import IntegrityError
from apps.reports.tasks import (create_messages_object,
                                get_messages_daily,
                                get_messages_monthly,
                                get_messages_yearly)
from datetime import date, datetime, timedelta
from django.urls import reverse
import json
from rest_framework.test import APIClient
import calendar


class TestMessagesReport():
    @pytest.mark.django_db
    def test_messages_create(self):
        messages = mixer.blend(MessagesReport)
        assert MessagesReport.objects.count() == 1
        assert messages.__str__() == ('{} - {}').format(
            messages.start_date.strftime("%d/%m/%Y"), messages.period)

    @pytest.mark.django_db
    def test_messages_integrity_error(self):
        content = mixer.blend(MessagesReport)
        with pytest.raises(IntegrityError) as excinfo:
            mixer.blend(MessagesReport,
                        period=content.period,
                        start_date=content.start_date)
        assert 'UNIQUE constraint failed' in str(
            excinfo.value)
        ## PostgreSQL message error
        # assert 'duplicate key value violates unique constraint' in str(
        #     excinfo.value)

    def test_create_messages_daily(self):
        data_daily = ['2020-11-23', 10]
        messages_object = create_messages_object(data_daily, 'daily')

        assert messages_object.period == 'daily'
        assert messages_object.start_date == '2020-11-23'
        assert messages_object.end_date == '2020-11-23'
        assert messages_object.messages == 10

    @pytest.mark.django_db
    def test_create_messages_monthly(self):
        data_monthly = {
            'month': date(2020, 1, 1),
            'total_messages': 10
        }

        messages_object = create_messages_object(data_monthly, 'monthly')

        assert messages_object.period == 'monthly'
        assert messages_object.start_date == date(2020, 1, 1)
        assert messages_object.end_date == date(2020, 1, 31)
        assert messages_object.messages == 10

    @pytest.mark.django_db
    def test_create_messages_yearly(self):
        data_yearly = {
            'year': date(2019, 1, 1),
            'total_messages': 10
        }

        messages_object = create_messages_object(data_yearly, 'yearly')

        assert messages_object.period == 'yearly'
        assert messages_object.start_date == date(2019, 1, 1)
        assert messages_object.end_date == date(2019, 12, 31)
        assert messages_object.messages == 10

    @pytest.mark.django_db
    def test_get_messages_daily_without_args(self):
        yesterday = datetime.now() - timedelta(days=1)
        active_room = mixer.blend(Room, is_active=True, is_visible=True)
        active_room.created = yesterday
        active_room.save()

        message = mixer.blend(Message, room=active_room)
        message.created = yesterday
        message.save()

        get_messages_daily.apply()

        daily_data = MessagesReport.objects.filter(
            period='daily').first()

        assert daily_data.start_date == yesterday.date()
        assert daily_data.end_date == yesterday.date()
        assert daily_data.period == 'daily'
        assert daily_data.messages == 1

    @pytest.mark.django_db
    def test_get_messages_monthly_without_args(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(MessagesReport, period='daily', messages=10,
                    start_date=yesterday, end_date=yesterday)

        get_messages_monthly.apply()

        monthly_data = MessagesReport.objects.filter(
            period='monthly').first()

        assert monthly_data.start_date == yesterday.replace(day=1)
        assert monthly_data.end_date == yesterday
        assert monthly_data.period == 'monthly'
        assert monthly_data.messages == 10

    @pytest.mark.django_db
    def test_get_messages_yearly_without_args(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(MessagesReport, period='monthly', messages=10,
                    start_date=yesterday.replace(day=1),
                    end_date=yesterday)

        get_messages_yearly.apply()

        yearly_data = MessagesReport.objects.filter(period='yearly').first()

        assert yearly_data.start_date == yesterday.replace(day=1, month=1)
        assert yearly_data.end_date == yesterday
        assert yearly_data.period == 'yearly'
        assert yearly_data.messages == 10

    @pytest.mark.django_db
    def test_get_messages_yearly_current_year(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(MessagesReport, period='monthly', messages=10,
                    start_date=yesterday.replace(day=1),
                    end_date=yesterday)
        mixer.blend(MessagesReport, period='yearly', messages=9,
                    start_date=yesterday.replace(day=1, month=1),
                    end_date=yesterday - timedelta(days=1))

        get_messages_yearly.apply()

        yearly_data = MessagesReport.objects.filter(period='yearly').first()

        assert yearly_data.start_date == yesterday.replace(day=1, month=1)
        assert yearly_data.end_date == yesterday
        assert yearly_data.period == 'yearly'
        assert yearly_data.messages == 10

    @pytest.mark.django_db
    def test_messages_api_url(api_client):
        mixer.cycle(5).blend(MessagesReport)
        url = reverse('messagesreport-list')
        client = APIClient()
        response = client.get(url)
        request = json.loads(response.content)

        assert response.status_code == 200
        assert request['count'] == 5
