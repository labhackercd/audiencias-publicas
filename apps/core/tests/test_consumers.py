import pytest
from django.urls import path
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from channels.routing import URLRouter
from apps.core.consumers.utils import get_room, get_data
from apps.core.consumers.home import HomeConsumer
from apps.core.consumers.room_questions import QuestionsPanelConsumer
from apps.core.consumers.room import RoomConsumer
from apps.core.utils import encrypt
from apps.core.models import Room, Question
from apps.accounts.models import User
from mixer.backend.django import mixer
from asgiref.sync import sync_to_async
import os

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}


@pytest.mark.django_db
def test_utils_get_room():
    room1 = mixer.blend(Room, is_active=True, pk=1)
    room2 = get_room(1)
    assert room1 == room2


@pytest.mark.django_db
def test_utils_get_room_value_error():
    with pytest.raises(ValueError):
        get_room('test')


@pytest.mark.django_db
def test_utils_get_room_not_exists():
    with pytest.raises(Room.DoesNotExist):
        get_room(1)


@pytest.mark.django_db
def test_utils_get_data():
    json_text = '{"text": "This is a test message."}'
    response = get_data(json_text)
    assert response == {'text': 'This is a test message.'}


@pytest.mark.django_db
def test_utils_get_data_value_error():
    with pytest.raises(ValueError):
        get_data('test')


@pytest.mark.asyncio
async def test_home_consumer(settings):
    
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    
    communicator = WebsocketCommunicator(
        HomeConsumer.as_asgi(), '/home/stream/')
    connected, _ = await communicator.connect()
    
    assert connected
    
    # Test sending text
    message = {
        'type': 'home.message',
        'text': 'This is a test message.',
    }
    
    channel_layer = get_channel_layer()
    
    await channel_layer.group_send('home', message=message)
    response = await communicator.receive_from()
    
    assert response == message['text']
    
    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_question_panel_consumer(settings):
    
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    
    room = await sync_to_async(
        mixer.blend)(Room, is_active=True, is_visible=True)

    application = URLRouter([
        path('sala/<int:room_id>/perguntas/stream/',
        QuestionsPanelConsumer.as_asgi()),
    ])

    communicator = WebsocketCommunicator(
        application,
        '/sala/%s/perguntas/stream/' % room.id)
    connected, _ = await communicator.connect()
    
    assert connected
    
    # Test sending text
    message = {
        'type': 'questions.panel',
        'text': 'This is a test message.',
    }
    
    channel_layer = get_channel_layer()
    
    await channel_layer.group_send(
        room.group_room_questions_name, message=message)
    response = await communicator.receive_from()
    
    assert response == message['text']
    
    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_room_consumer():
    room = await sync_to_async(
        mixer.blend)(Room, is_active=True, is_visible=True)
    user = await sync_to_async(
        mixer.blend)(User, is_active=True)

    application = URLRouter([
        path('sala/<int:room_id>/stream/',
        RoomConsumer.as_asgi()),
    ])

    communicator = WebsocketCommunicator(
        application,
        '/sala/%s/stream/' % room.id)
    communicator.scope['user'] = user
    connected, _ = await communicator.connect()
    
    assert connected

    handler = encrypt(str(user.id).rjust(10))
    question = await sync_to_async(
        mixer.blend)(Question, room=room)

    # Test send vote
    new_vote_data = {
        'handler': handler,
        'question': question.id,
        'is_vote': True,
    }
    
    await communicator.send_json_to(data=new_vote_data)
    response = await communicator.receive_json_from(timeout=5)
    assert response['user'] == handler
    assert len(response['voteList']) == 1
    
    # Test remove vote
    await communicator.send_json_to(data=new_vote_data)
    response = await communicator.receive_json_from(timeout=5)
    assert response['user'] == handler
    assert len(response['voteList']) == 0

    # Test send message
    new_message_data = {
        'handler': handler,
        'message': 'Test message',
    }
    
    await communicator.send_json_to(data=new_message_data)
    response = await communicator.receive_json_from(timeout=5)
    assert response['chat'] == True

    # Test send question
    new_question_data = {
        'handler': handler,
        'question': 'Test pederasta?',
        'is_vote': False,
    }
    
    await communicator.send_json_to(data=new_question_data)
    response = await communicator.receive_json_from(timeout=5)
    assert response['user'] == handler
    assert response['question'] == True

    # Close
    await communicator.disconnect()
