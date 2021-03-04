import pytest
from mixer.backend.django import mixer
from apps.core.models import Room
from django.urls import reverse
import json
from rest_framework.test import APIClient


class TestRankingReport():
    @pytest.mark.django_db
    def test_ranking_api_url(api_client):
        mixer.cycle(5).blend(Room, is_active=True, is_visible=True)
        url = reverse('ranking-list')
        client = APIClient()
        response = client.get(url)
        request = json.loads(response.content)

        assert response.status_code == 200
        assert request['count'] == 5
