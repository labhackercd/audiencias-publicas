import pytest
from channels.testing import WebsocketCommunicator
from apps.core.consumers.home import HomeConsumer
from channels.layers import get_channel_layer

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
