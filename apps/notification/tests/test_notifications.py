import pytest
from mixer.backend.django import mixer
from apps.notification.models import ParticipantNotification
from apps.core.models import Room, Message
from apps.accounts.models import User, UserProfile
from django.urls import reverse
from django.conf import settings


class TestParticipantNotification():

    def test_apps(self):
        from apps.notification.apps import NotificationConfig
        assert NotificationConfig.name == 'apps.notification'

    @pytest.mark.django_db
    def test_notification_create(self):
        room = mixer.blend(Room, title_reunion='Title test')
        notification = mixer.blend(ParticipantNotification, room=room)
        assert ParticipantNotification.objects.count() == 1
        assert notification.__str__() == 'Title test'

    @pytest.mark.django_db
    def test_delete_room_with_notification(self):
        room = mixer.blend(Room, title_reunion='Title test')
        mixer.blend(ParticipantNotification, room=room)
        room.delete()
        assert ParticipantNotification.objects.count() == 0
    
    @pytest.mark.django_db
    def test_send_participants_notification(self, client, mailoutbox):
        room = mixer.blend(Room, is_active=True)
        mixer.blend(Message, room=room)

        user = mixer.blend(User, is_active=True)
        UserProfile.objects.create(user=user, is_admin=True)
        
        settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
        client.force_login(user)
        url = reverse('participants_notification', args=[room.id])
        data = {'subject': 'subject test', 'content': 'content test'}
        response = client.post(url, data=data)

        assert response.status_code == 302
        assert len(mailoutbox) == 1
        assert ParticipantNotification.objects.count() == 1

    @pytest.mark.django_db
    def test_send_participants_notification_without_permission(self, client):
        room = mixer.blend(Room, is_active=True)
        user = mixer.blend(User, is_active=True)

        client.force_login(user)
        url = reverse('participants_notification', args=[room.id])
        data = {'subject': 'subject test', 'content': 'content test'}
        response = client.post(url, data=data)

        assert response.status_code == 404
