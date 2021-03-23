import pytest
from mixer.backend.django import mixer
from apps.reports.models import RoomsReport
from apps.core.models import Room
from django.db import IntegrityError
from apps.reports.tasks import (create_rooms_object,
                                get_rooms_daily,
                                get_rooms_monthly,
                                get_rooms_yearly)
from datetime import date, datetime, timedelta
from django.urls import reverse
import json
from rest_framework.test import APIClient
import calendar


class TestRoomsReport():
    @pytest.mark.django_db
    def test_rooms_create(self):
        rooms = mixer.blend(RoomsReport)
        assert RoomsReport.objects.count() == 1
        assert rooms.__str__() == ('{} - {}').format(
            rooms.start_date.strftime("%d/%m/%Y"), rooms.period)

    @pytest.mark.django_db
    def test_rooms_integrity_error(self):
        content = mixer.blend(RoomsReport)
        with pytest.raises(IntegrityError) as excinfo:
            mixer.blend(RoomsReport,
                        period=content.period,
                        start_date=content.start_date)
        assert 'UNIQUE constraint failed' in str(
            excinfo.value)
        ## PostgreSQL message error
        # assert 'duplicate key value violates unique constraint' in str(
        #     excinfo.value)

    def test_create_rooms_daily(self):
        data_daily = ['2020-11-23', 10]
        rooms_object = create_rooms_object(data_daily, 'daily')

        assert rooms_object.period == 'daily'
        assert rooms_object.start_date == '2020-11-23'
        assert rooms_object.end_date == '2020-11-23'
        assert rooms_object.rooms == 10

    @pytest.mark.django_db
    def test_create_rooms_monthly(self):
        data_monthly = {
            'month': date(2020, 1, 1),
            'total_rooms': 10
        }

        rooms_object = create_rooms_object(data_monthly, 'monthly')

        assert rooms_object.period == 'monthly'
        assert rooms_object.start_date == date(2020, 1, 1)
        assert rooms_object.end_date == date(2020, 1, 31)
        assert rooms_object.rooms == 10

    @pytest.mark.django_db
    def test_create_rooms_yearly(self):
        data_yearly = {
            'year': date(2019, 1, 1),
            'total_rooms': 10
        }

        rooms_object = create_rooms_object(data_yearly, 'yearly')

        assert rooms_object.period == 'yearly'
        assert rooms_object.start_date == date(2019, 1, 1)
        assert rooms_object.end_date == date(2019, 12, 31)
        assert rooms_object.rooms == 10

    @pytest.mark.django_db
    def test_get_rooms_daily_without_args(self):
        yesterday = datetime.now() - timedelta(days=1)
        room = mixer.blend(Room, is_active=True, is_visible=True)
        room.created = yesterday
        room.save()

        get_rooms_daily.apply()

        daily_data = RoomsReport.objects.filter(
            period='daily').first()

        assert daily_data.start_date == yesterday.date()
        assert daily_data.end_date == yesterday.date()
        assert daily_data.period == 'daily'
        assert daily_data.rooms == 1

    @pytest.mark.django_db
    def test_get_rooms_monthly_without_args(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(RoomsReport, period='daily', rooms=10,
                    start_date=yesterday, end_date=yesterday)

        get_rooms_monthly.apply()

        monthly_data = RoomsReport.objects.filter(
            period='monthly').first()

        assert monthly_data.start_date == yesterday.replace(day=1)
        assert monthly_data.end_date == yesterday
        assert monthly_data.period == 'monthly'
        assert monthly_data.rooms == 10

    @pytest.mark.django_db
    def test_get_rooms_yearly_without_args(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(RoomsReport, period='monthly', rooms=10,
                    start_date=yesterday.replace(day=1),
                    end_date=yesterday)

        get_rooms_yearly.apply()

        yearly_data = RoomsReport.objects.filter(period='yearly').first()

        assert yearly_data.start_date == yesterday.replace(day=1, month=1)
        assert yearly_data.end_date == yesterday
        assert yearly_data.period == 'yearly'
        assert yearly_data.rooms == 10

    @pytest.mark.django_db
    def test_get_rooms_yearly_current_year(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(RoomsReport, period='monthly', rooms=10,
                    start_date=yesterday.replace(day=1),
                    end_date=yesterday)
        mixer.blend(RoomsReport, period='yearly', rooms=9,
                    start_date=yesterday.replace(day=1, month=1),
                    end_date=yesterday - timedelta(days=1))

        get_rooms_yearly.apply()

        yearly_data = RoomsReport.objects.filter(period='yearly').first()

        assert yearly_data.start_date == yesterday.replace(day=1, month=1)
        assert yearly_data.end_date == yesterday
        assert yearly_data.period == 'yearly'
        assert yearly_data.rooms == 10

    @pytest.mark.django_db
    def test_rooms_api_url(api_client):
        mixer.cycle(5).blend(RoomsReport)
        url = reverse('roomsreport-list')
        client = APIClient()
        response = client.get(url)
        request = json.loads(response.content)

        assert response.status_code == 200
        assert request['count'] == 5
