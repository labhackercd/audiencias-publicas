import pytest
from mixer.backend.django import mixer
from apps.core.models import Room
from django.urls import reverse
import json
from rest_framework.test import APIClient
from datetime import date, timedelta


class TestRankingReport():
    @pytest.mark.django_db
    def test_ranking_api_url(api_client):
        yesterday = date.today() - timedelta(days=1)
        mixer.cycle(5).blend(Room, date=yesterday)
        url = reverse('ranking-list')
        client = APIClient()
        response = client.get(url)
        request = json.loads(response.content)

        assert response.status_code == 200
        assert request['count'] == 5
