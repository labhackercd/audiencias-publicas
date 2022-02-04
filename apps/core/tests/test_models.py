import pytest
from mixer.backend.django import mixer
from apps.core.models import *
from datetime import datetime, timedelta
from django.urls import reverse
from django.utils import timezone
from constance import config as constance_config


@pytest.fixture
def test_user(db, django_user_model):
    return django_user_model.objects.create_user(
        username='testuser', email='test@e.com', is_active=True)


@pytest.mark.django_db
def test_room_with_title():
    room = mixer.blend(Room, title_reunion='title test')
    assert room.__str__() == 'title test'


@pytest.mark.django_db
def test_room_without_title():
    room = mixer.blend(Room, title_reunion='')
    assert room.__str__() == 'room'


@pytest.mark.django_db
def test_room_is_today():
    room = mixer.blend(Room, date=datetime.now())
    assert room.is_today() == True
    assert room.is_tomorrow() == False


@pytest.mark.django_db
def test_room_is_tomorrow():
    room = mixer.blend(Room, date=datetime.now() + timedelta(days=1))
    assert room.is_today() == False
    assert room.is_tomorrow() == True


@pytest.mark.django_db
def test_room_time_to_close():
    room = mixer.blend(Room, closed_time=timezone.now(), youtube_status=2)
    assert room.time_to_close() < 900 # 15 minutes


@pytest.mark.django_db
def test_room_without_time_to_close():
    room = mixer.blend(Room, closed_time=None)
    assert room.time_to_close() == False


@pytest.mark.django_db
def test_room_main_video():
    room = mixer.blend(Room)
    video = mixer.blend(Video, room=room, is_attachment=False)
    assert room.latest_video() == video
    assert room.get_main_videos().count() == 1


@pytest.mark.django_db
def test_room_attachment_video():
    room = mixer.blend(Room)
    mixer.blend(Video, room=room, is_attachment=True)
    assert room.get_attachment_videos().count() == 1


@pytest.mark.django_db
def test_room_without_video():
    with pytest.raises(Video.DoesNotExist):
        room = mixer.blend(Room)
        room.latest_video()


@pytest.mark.django_db
def test_room_get_absolute_url():
    room = mixer.blend(Room)
    assert room.get_absolute_url() == reverse(
        'video_room', kwargs={'pk': room.id})


@pytest.mark.django_db
def test_room_properties(test_user):
    room = mixer.blend(Room)
    question = mixer.blend(Question, user=test_user, room=room)
    mixer.blend(Message, user=test_user, room=room)
    mixer.blend(UpDownVote, user=test_user, question=question)
    assert room.questions_count == 1
    assert room.messages_count == 1
    assert room.votes_count == 1
    assert room.participants_count == 1


@pytest.mark.django_db
def test_vote_create(test_user):
    vote = mixer.blend(UpDownVote, user=test_user)
    assert vote.__str__() == 'testuser'


@pytest.mark.django_db
def test_message_create():
    message = mixer.blend(Message, message='test message')
    assert message.__str__() == 'test message'


@pytest.mark.django_db
def test_video_create():
    video = mixer.blend(Video, video_id='testId')
    assert video.__str__() == 'testId'


@pytest.mark.django_db
def test_question_create():
    question = mixer.blend(Question, question='test question?')
    assert question.__str__() == 'test question?'


@pytest.mark.django_db
def test_room_attachment_create():
    room = mixer.blend(Room, title_reunion='title test')
    attachment = mixer.blend(RoomAttachment, room=room)
    assert attachment.__str__() == 'title test'


@pytest.mark.django_db
@pytest.mark.enable_signals
def test_room_video_signals(test_user):
    constance_keys = {
        'WELCOME_MESSAGE': 'test message',
        'WELCOME_MESSAGE_USER_ID': test_user.id,
        'WELCOME_VIDEO': 'testVideoId',
        'WELCOME_VIDEO_TITLE': 'test video title'
    }
    for key, value in constance_keys.items():
        setattr(constance_config, key, value)

    room = mixer.blend(Room, youtube_status=2)
    message = Message.objects.filter(room=room, user=test_user).first()
    video = Video.objects.filter(room=room).first()

    assert message.message == 'test message'
    assert message.user == test_user
    assert video.video_id == 'testVideoId'
    assert video.title == 'test video title'

    video.delete()

    assert room.videos.count() == 0

