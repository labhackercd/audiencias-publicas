import pytest
from mixer.backend.django import mixer
from apps.accounts.models import User
from django.test.client import RequestFactory
from apps.accounts.backends import AudienciasAuthBackend
import json


@pytest.mark.django_db
def test_remote_user_authenticate():
    user = mixer.blend(
        User, username='testuser', email='test@e.com', is_active=True)
    user_data = {
        'email': 'test@e.com',
        'first_name': 'test',
        'last_name': 'user'}
    request = RequestFactory().get('/')
    request.META['HTTP_REMOTE_USER_DATA'] = json.dumps(user_data)
    auth_backend = AudienciasAuthBackend()
    authenticated_user = auth_backend.authenticate(
        request, user.username)

    assert user == authenticated_user


def test_no_remote_user_authenticate():
    request = RequestFactory().get('/')
    auth_backend = AudienciasAuthBackend()
    authenticated_user = auth_backend.authenticate(request, '')

    assert authenticated_user == None
