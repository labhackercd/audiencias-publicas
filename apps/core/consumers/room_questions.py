from channels.generic.websocket import AsyncWebsocketConsumer
from apps.core.models import Room

import logging

log = logging.getLogger("chat")


class QuestionsPanelConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        room_id = self.scope['url_route']['kwargs']['room_id']
        room = Room.objects.get(id=room_id)
        self.group_name = room.group_room_questions_name
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        log.debug('Questions panel websocket connected.')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        log.debug('Questions panel websocket disconnected. Code:', close_code)

    async def questions_panel(self, event):
        await self.send(text_data=event["text"])
