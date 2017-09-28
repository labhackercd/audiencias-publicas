from django.test import TestCase, Client
from autofixture import AutoFixture
from apps.core.models import Room


class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.room_fixture = AutoFixture(Room)

    def test_token_permission(self):
        with self.settings(SECRET_KEY="key"):
            response = self.client.get('/api/user/?api_key=key')
            self.assertEqual(response.status_code, 200)
            response = self.client.get('/api/user/?api_key=another_key')
            self.assertEqual(response.status_code, 403)

    def test_room_api(self):
        room = self.room_fixture.create_one()
        response = self.client.get('/api/room/%s' % room.pk)
        self.assertEqual(response.status_code, 200)

    def test_api_root(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
