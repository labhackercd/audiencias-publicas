import pytest
from mixer.backend.django import mixer
from apps.accounts.models import User, UserProfile
from django.contrib.auth.models import AnonymousUser
from django.test.client import RequestFactory
from apps.accounts.backends import AudienciasAuthBackend
from apps.accounts.middlewares import AudienciasRemoteUser
from django.test import Client
from django.core.exceptions import ImproperlyConfigured
from django.contrib import auth
import json
from django.conf import settings

TEST_AUTHENTICATION_BACKENDS = (
    'apps.accounts.backends.AudienciasAuthBackend',
)

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


@pytest.mark.django_db
def test_user_no_remote_user_middleware():
    user = mixer.blend(User, username='testuser', is_active=True)

    request = RequestFactory().get('/')
    request.user = user
    auth_middleware = AudienciasRemoteUser()
    response = auth_middleware.process_request(request)

    assert response == None


@pytest.mark.django_db
def test_invalid_username_remote_user_middleware():
    user = mixer.blend(User, username='testuser', is_active=True)
    client = Client()
    client.force_login(user)
    request = RequestFactory().get('/')
    request.user = user
    request.META['HTTP_AUTH_USER'] = 'invaliduser'
    request.session = client.session
    auth_middleware = AudienciasRemoteUser()
    response = auth_middleware.process_request(request)

    assert response == None


@pytest.mark.django_db
def test_utils_get_room_value_error():
    with pytest.raises(ImproperlyConfigured):
        request = RequestFactory().get('/')
        auth_middleware = AudienciasRemoteUser()
        auth_middleware.process_request(request)


@pytest.mark.django_db
def test_valid_username_authenticated_middleware():
    user = mixer.blend(User, username='testuser', is_active=True)
    client = Client()
    client.force_login(user)
    request = RequestFactory().get('/')
    request.user = user
    request.META['HTTP_AUTH_USER'] = 'testuser'
    request.session = client.session
    auth_middleware = AudienciasRemoteUser()
    response = auth_middleware.process_request(request)

    assert response == None


@pytest.mark.django_db
def test_force_logout_if_no_header_middleware():
    user = mixer.blend(User, username='testuser', is_active=True)
    client = Client()
    client.force_login(user)
    request = RequestFactory().get('/')
    request.user = user
    request.session = client.session
    auth_middleware = AudienciasRemoteUser()
    auth_middleware.force_logout_if_no_header = True
    response = auth_middleware.process_request(request)

    assert response == None


@pytest.mark.django_db
def test_remove_invalid_user_no_session_key():
    with pytest.raises(ImportError):
        user = mixer.blend(User, username='testuser', is_active=True)
        client = Client()
        client.force_login(user)
        request = RequestFactory().get('/')
        request.user = user
        request.session = client.session
        del request.session[auth.BACKEND_SESSION_KEY]
        auth_middleware = AudienciasRemoteUser()
        auth_middleware.force_logout_if_no_header = True
        auth_middleware.process_request(request)


@pytest.mark.django_db
def test_remove_invalid_user_invalid_session_key():
    settings.AUTHENTICATION_BACKENDS = TEST_AUTHENTICATION_BACKENDS
    backend_path = 'apps.accounts.backends.AudienciasAuthBackend'
    user = mixer.blend(User, username='testuser', is_active=True)
    client = Client()
    client.force_login(user)
    request = RequestFactory().get('/')
    request.user = user
    request.session = client.session
    request.session[auth.BACKEND_SESSION_KEY] = backend_path
    auth_middleware = AudienciasRemoteUser()
    auth_middleware.force_logout_if_no_header = True
    response = auth_middleware.process_request(request)

    assert response == None


@pytest.mark.django_db
def test_valid_username_unauthenticated_middleware():
    from django.contrib.sessions.middleware import SessionMiddleware
    settings.AUTHENTICATION_BACKENDS = TEST_AUTHENTICATION_BACKENDS
    backend_path = 'apps.accounts.backends.AudienciasAuthBackend'
    mixer.blend(User, username='testuser', email='test@e.com', is_active=True)
    user_data = {
        'email': 'test@e.com',
        'avatar': '/media/img/avatar.png',
        'first_name': 'test',
        'last_name': 'user'}
    request = RequestFactory().get('/')
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()
    request.session[auth.BACKEND_SESSION_KEY] = backend_path
    request.user = AnonymousUser()
    request.META['HTTP_AUTH_USER'] = 'testuser'
    request.META['HTTP_REMOTE_USER_DATA'] = json.dumps(user_data)
    auth_middleware = AudienciasRemoteUser()
    auth_middleware.process_request(request)
    user = User.objects.get(username='testuser')

    assert user.first_name == 'test'
    assert user.last_name == 'user'
    assert user.profile.avatar_url == '/media/img/avatar.png'


@pytest.mark.django_db
def test_valid_username_unauthenticated_with_profile_middleware():
    from django.contrib.sessions.middleware import SessionMiddleware
    settings.AUTHENTICATION_BACKENDS = TEST_AUTHENTICATION_BACKENDS
    backend_path = 'apps.accounts.backends.AudienciasAuthBackend'
    existing_user = mixer.blend(User,
        username='testuser', email='test@e.com', is_active=True)
    mixer.blend(UserProfile, user=existing_user)
    user_data = {
        'email': 'test@e.com',
        'avatar': '/media/img/avatar.png',
        'first_name': 'test',
        'last_name': 'user'}
    request = RequestFactory().get('/')
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()
    request.session[auth.BACKEND_SESSION_KEY] = backend_path
    request.user = AnonymousUser()
    request.META['HTTP_AUTH_USER'] = 'testuser'
    request.META['HTTP_REMOTE_USER_DATA'] = json.dumps(user_data)
    auth_middleware = AudienciasRemoteUser()
    auth_middleware.process_request(request)
    user = User.objects.get(username='testuser')

    assert user.first_name == 'test'
    assert user.last_name == 'user'
    assert user.profile.avatar_url == '/media/img/avatar.png'