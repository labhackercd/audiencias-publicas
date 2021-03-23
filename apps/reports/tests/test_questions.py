import pytest
from mixer.backend.django import mixer
from apps.reports.models import QuestionsReport
from apps.core.models import Question, Room
from django.db import IntegrityError
from apps.reports.tasks import (create_questions_object,
                                get_questions_daily,
                                get_questions_monthly,
                                get_questions_yearly)
from datetime import date, datetime, timedelta
from django.urls import reverse
import json
from rest_framework.test import APIClient
import calendar


class TestQuestionsReport():
    @pytest.mark.django_db
    def test_questions_create(self):
        questions = mixer.blend(QuestionsReport)
        assert QuestionsReport.objects.count() == 1
        assert questions.__str__() == ('{} - {}').format(
            questions.start_date.strftime("%d/%m/%Y"), questions.period)

    @pytest.mark.django_db
    def test_questions_integrity_error(self):
        content = mixer.blend(QuestionsReport)
        with pytest.raises(IntegrityError) as excinfo:
            mixer.blend(QuestionsReport,
                        period=content.period,
                        start_date=content.start_date)
        assert 'UNIQUE constraint failed' in str(
            excinfo.value)
        ## PostgreSQL message error
        # assert 'duplicate key value violates unique constraint' in str(
        #     excinfo.value)

    def test_create_questions_daily(self):
        data_daily = ['2020-11-23', 10]
        questions_object = create_questions_object(data_daily, 'daily')

        assert questions_object.period == 'daily'
        assert questions_object.start_date == '2020-11-23'
        assert questions_object.end_date == '2020-11-23'
        assert questions_object.questions == 10

    @pytest.mark.django_db
    def test_create_questions_monthly(self):
        data_monthly = {
            'month': date(2020, 1, 1),
            'total_questions': 10
        }

        questions_object = create_questions_object(data_monthly, 'monthly')

        assert questions_object.period == 'monthly'
        assert questions_object.start_date == date(2020, 1, 1)
        assert questions_object.end_date == date(2020, 1, 31)
        assert questions_object.questions == 10

    @pytest.mark.django_db
    def test_create_questions_yearly(self):
        data_yearly = {
            'year': date(2019, 1, 1),
            'total_questions': 10
        }

        questions_object = create_questions_object(data_yearly, 'yearly')

        assert questions_object.period == 'yearly'
        assert questions_object.start_date == date(2019, 1, 1)
        assert questions_object.end_date == date(2019, 12, 31)
        assert questions_object.questions == 10

    @pytest.mark.django_db
    def test_get_questions_daily_without_args(self):
        yesterday = datetime.now() - timedelta(days=1)
        active_room = mixer.blend(Room, is_active=True, is_visible=True)
        active_room.created = yesterday
        active_room.save()

        question = mixer.blend(Question, room=active_room)
        question.created = yesterday
        question.save()

        get_questions_daily.apply()

        daily_data = QuestionsReport.objects.filter(
            period='daily').first()

        assert daily_data.start_date == yesterday.date()
        assert daily_data.end_date == yesterday.date()
        assert daily_data.period == 'daily'
        assert daily_data.questions == 1

    @pytest.mark.django_db
    def test_get_questions_monthly_without_args(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(QuestionsReport, period='daily', questions=10,
                    start_date=yesterday, end_date=yesterday)

        get_questions_monthly.apply()

        monthly_data = QuestionsReport.objects.filter(
            period='monthly').first()

        assert monthly_data.start_date == yesterday.replace(day=1)
        assert monthly_data.end_date == yesterday
        assert monthly_data.period == 'monthly'
        assert monthly_data.questions == 10

    @pytest.mark.django_db
    def test_get_questions_yearly_without_args(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(QuestionsReport, period='monthly', questions=10,
                    start_date=yesterday.replace(day=1),
                    end_date=yesterday)

        get_questions_yearly.apply()

        yearly_data = QuestionsReport.objects.filter(period='yearly').first()

        assert yearly_data.start_date == yesterday.replace(day=1, month=1)
        assert yearly_data.end_date == yesterday
        assert yearly_data.period == 'yearly'
        assert yearly_data.questions == 10

    @pytest.mark.django_db
    def test_get_questions_yearly_current_year(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(QuestionsReport, period='monthly', questions=10,
                    start_date=yesterday.replace(day=1),
                    end_date=yesterday)
        mixer.blend(QuestionsReport, period='yearly', questions=9,
                    start_date=yesterday.replace(day=1, month=1),
                    end_date=yesterday - timedelta(days=1))

        get_questions_yearly.apply()

        yearly_data = QuestionsReport.objects.filter(period='yearly').first()

        assert yearly_data.start_date == yesterday.replace(day=1, month=1)
        assert yearly_data.end_date == yesterday
        assert yearly_data.period == 'yearly'
        assert yearly_data.questions == 10

    @pytest.mark.django_db
    def test_questions_api_url(api_client):
        mixer.cycle(5).blend(QuestionsReport)
        url = reverse('questionsreport-list')
        client = APIClient()
        response = client.get(url)
        request = json.loads(response.content)

        assert response.status_code == 200
        assert request['count'] == 5
