import pytest
from mixer.backend.django import mixer
from apps.core.models import Room
from apps.core.permissions import ApiKeyPermission
from apps.accounts.models import User
from django.urls import reverse
from django.conf import settings
from django.test import RequestFactory



def test_reports_api_root_url(client):
    url = reverse('api_root')
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_rooms_api(client):
    mixer.cycle(5).blend(Room)
    url = reverse('room-list')
    response = client.get(url, format='json')

    assert response.status_code == 200
    assert response.data['count'] == 5
    assert response.data['results'][0]['answered_questions_count'] == 0


@pytest.mark.django_db
def test_users_api(client):
    mixer.blend(User, username='testuser', email='test@e.com', is_active=True)
    url = reverse('user-list')
    response = client.get(url, format='json')

    assert response.status_code == 200
    assert response.data['count'] == 1


def test_permissions_unsafe_method_api():
    request = RequestFactory().put('/')
    permission_check = ApiKeyPermission()
    permission = permission_check.has_permission(request, None)

    assert permission == False
