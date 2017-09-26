from django.utils.translation import ugettext_lazy as _
from django.test import TestCase, Client
from autofixture import AutoFixture
from apps.core import models
from apps.accounts.models import User
from freezegun import freeze_time
import datetime


class ModelsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.room_fixture = AutoFixture(models.Room, field_values={
            'date': datetime.datetime(2017, 9, 24),
            'youtube_status': 2,
            'is_visible': True
        })
        self.user_fixture = AutoFixture(User, field_values={
            'first_name': 'Michael',
            'last_name': 'Douglas'
        })
        self.vote_fixture = AutoFixture(models.UpDownVote, generate_fk=True)
        self.message_fixture = AutoFixture(models.Message, generate_fk=True)
        self.question_fixture = AutoFixture(models.Question, generate_fk=True)

    def test_room_str(self):
        room1 = self.room_fixture.create_one()
        room1.legislative_body_alias = 'ESPORTE'
        room1.save()
        room2 = self.room_fixture.create_one()
        room2.legislative_body_alias = ''
        room2.title_reunion = 'Audiêcia Pública'
        room2.save()
        room3 = self.room_fixture.create_one()
        room3.legislative_body_alias = ''
        room3.title_reunion = ''
        room2.save()
        self.assertEquals(room1.__str__(), 'ESPORTE')
        self.assertEquals(room2.__str__(), 'Audiêcia Pública')
        self.assertEquals(room3.__str__(), _('room'))

    @freeze_time("2017-09-24")
    def test_room_is_today(self):
        room1 = self.room_fixture.create_one()
        room2 = self.room_fixture.create_one()
        room2.date = datetime.datetime(2017, 9, 23)
        room2.save()
        self.assertEquals(room1.is_today(), True)
        self.assertEquals(room2.is_today(), False)

    @freeze_time("2017-09-23")
    def test_room_is_tomorrow(self):
        room1 = self.room_fixture.create_one()
        room2 = self.room_fixture.create_one()
        room2.date = datetime.datetime(2017, 9, 23)
        room2.save()
        self.assertEquals(room1.is_tomorrow(), True)
        self.assertEquals(room2.is_tomorrow(), False)

    def test_room_get_absolute_url(self):
        room = self.room_fixture.create_one()
        with self.settings(FORCE_SCRIPT_NAME="audiencias"):
            self.assertEquals(room.get_absolute_url(),
                              "audiencias/sala/%s" % room.pk)

    @freeze_time("2017-09-25")
    def test_room_html_body(self):
        room = self.room_fixture.create_one()
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'includes/home_video.html')
        self.assertContains(response, room.html_body())

    @freeze_time("2017-09-25")
    def test_room_html_room_video(self):
        room = self.room_fixture.create_one()
        response = self.client.get('/sala/%s' % room.pk)
        self.assertTemplateUsed(response, 'includes/room_video.html')
        self.assertContains(response, room.html_room_video())

    def test_room_group_room_name(self):
        room = self.room_fixture.create_one()
        self.assertEquals(room.group_room_name, "room-%s" % room.pk)

    def test_room_group_room_questions_name(self):
        room = self.room_fixture.create_one()
        self.assertEquals(room.group_room_questions_name,
                          "video-room-questions-%s" % room.pk)

    def test_room_send_video(self):
        room = self.room_fixture.create_one()
        room.send_video()

    def test_vote_str(self):
        user = self.user_fixture.create_one()
        vote = self.vote_fixture.create_one()
        vote.user = user
        vote.save()
        self.assertEquals(vote.__str__(), 'Michael Douglas')

    def test_message_str(self):
        message = self.message_fixture.create_one()
        message.message = 'Teste'
        message.save()
        self.assertEquals(message.__str__(), 'Teste')

    def test_message_html_body(self):
        message = self.message_fixture.create_one()
        response = self.client.get('/sala/%s' % message.room.pk)
        self.assertTemplateUsed(response, 'includes/chat_message.html')
        self.assertContains(response, message.html_body())

    def test_question_str(self):
        question = self.question_fixture.create_one()
        question.question = 'Teste'
        question.save()
        self.assertEquals(question.__str__(), 'Teste')
