from channels.generic.websocket import AsyncWebsocketConsumer
import logging

log = logging.getLogger("ws-logger")

class HomeConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = 'home'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        log.info('Home websocket connected.')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        log.info('Home websocket disconnected. Code: %s' % close_code)

    async def home_message(self, event):
        await self.send(text_data=event["text"])
