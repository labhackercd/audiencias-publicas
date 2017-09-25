from django.test import TestCase, Client
from apps.core import models
from freezegun import freeze_time
import datetime


class ModelsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.room = models.Room.objects.create(
            cod_reunion="10",
            cod_audio="11",
            title_reunion="Audiência Pública",
            legislative_body_initials="CESPO",
            legislative_body_alias="ESPORTE",
            legislative_body="Comissão do Esporte",
            reunion_status=3,
            reunion_type="Audiência Pública",
            reunion_object="Pauta da reunião",
            reunion_theme="Debater a aposentadoria dos atletas",
            location="Plenário 2",
            is_joint=False,
            youtube_status=1,
            youtube_id="videoId123",
            date=datetime.datetime(2017, 9, 24, 19, 0),
            online_users=10,
            max_online_users=11,
            views=12,
            is_visible=True)

    def test_room_str(self):
        self.assertEquals(self.room.__str__(), 'ESPORTE')

    @freeze_time("2017-09-24")
    def test_room_is_today(self):
        self.assertEquals(self.room.is_today(), True)

    @freeze_time("2017-09-23")
    def test_room_is_tomorrow(self):
        self.assertEquals(self.room.is_tomorrow(), True)

    def test_room_get_absolute_url(self):
        with self.settings(FORCE_SCRIPT_NAME="audiencias"):
            self.assertEquals(self.room.get_absolute_url(),
                              "audiencias/sala/%s" % self.room.pk)

    def test_room_html_body(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'includes/home_video.html')
        self.assertContains(response, 'data-video-id="%s"' % self.room.pk)

    def test_room_html_room_video(self):
        response = self.client.get('/sala/%s' % self.room.pk)
        self.assertTemplateUsed(response, 'includes/room_video.html')
        self.assertContains(response, 'class="video__iframe" id="player"')

    def test_room_group_room_name(self):
        self.assertEquals(self.room.group_room_name, "room-%s" % self.room.pk)

    def test_room_group_room_questions_name(self):
        self.assertEquals(self.room.group_room_questions_name,
                          "video-room-questions-%s" % self.room.pk)
