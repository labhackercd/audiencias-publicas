import pytest
from channels.testing import WebsocketCommunicator
from apps.core.consumers.home import HomeConsumer
from apps.core.consumers.room_questions import QuestionsPanelConsumer
from channels.layers import get_channel_layer
from mixer.backend.django import mixer
from apps.core.models import Room
from asgiref.sync import sync_to_async
from channels.routing import URLRouter
from django.urls import path
import os

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}


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
@pytest.mark.django_db
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
