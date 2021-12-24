import json
import logging
import re
from apps.core.models import Message, Question, UpDownVote, Room
from apps.core.utils import decrypt, encrypt
from apps.core.consumers.utils import get_room, get_data
from constance import config
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from channels_presence.models import Room as RoomPresence
from channels_presence.decorators import touch_presence
from channels.db import database_sync_to_async

User = get_user_model()
log = logging.getLogger('ws-logger')


@database_sync_to_async
def set_max_online_users(room, group_name, channel_name, user):
    room_presence = RoomPresence.objects.add(
        group_name, channel_name, user)
    anonymous_count = room_presence.get_anonymous_count()
    users_count = room_presence.get_users().count()
    room.online_users = anonymous_count + users_count
    if room.online_users > room.max_online_users:
        room.max_online_users = room.online_users
    room.save(update_fields=['online_users', 'max_online_users'])


@database_sync_to_async
def set_user_offline(room, group_name, channel_name):
    RoomPresence.objects.remove(group_name, channel_name)
    room.online_users -= 1
    room.save(update_fields=['online_users'])


@database_sync_to_async
def get_user_by_handler(handler):
    user = User.objects.get(id=decrypt(handler))
    return user


@database_sync_to_async
def create_voted_question(room, user, query):
    question = Question.objects.create(
        room=room, user=user, question=query)
    UpDownVote.objects.create(
        question=question, user=user, vote=True)
    return question


@database_sync_to_async
def create_chat_message(room, user, message_text):
    message = Message.objects.create(
        room=room, user=user, message=message_text)
    return message


@database_sync_to_async
def toggle_vote(question_id, user):
    question = Question.objects.get(id=question_id)
    if question.user != user:
        vote, created = UpDownVote.objects.get_or_create(
            user=user, question=question, vote=True)

        if not created:
            vote.delete()
    return question


def clean_text(text):
    blackList = [x.strip() for x in config.WORDS_BLACK_LIST.split(',')]
    wordList = re.sub(
        "[^\w]", " ", text.lower()).split()
    censured_words = list(set(blackList) & set(wordList))

    if censured_words:
        for word in censured_words:
            text = re.sub(
                word, '♥', text, flags=re.IGNORECASE)
    
    return text


class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_id = self.scope['url_route']['kwargs']['room_id']
        self.room = await database_sync_to_async(Room.objects.get)(id=room_id)
        self.group_name = self.room.group_room_name
        self.user = self.scope['user']

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        if self.room is not None:
            await set_max_online_users(
                self.room, self.group_name, self.channel_name, self.user)
            log.info('Room websocket connected.')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await set_user_offline(self.room, self.group_name, self.channel_name)
        log.info('Room websocket disconnected. Code: %s' % close_code)

    @touch_presence
    async def receive(self, text_data=None, bytes_data=None):
        data = get_data(text_data)

        if 'handler' in data.keys():
            user = await get_user_by_handler(data['handler'])
        else:
            return # pragma: no cover

        if set(data.keys()) == set(('handler', 'question', 'is_vote')):    
            if data['is_vote']:
                question = await toggle_vote(data['question'], user)
            else:
                if len(data['question']) <= 300 and data['question'].strip():
                    question_text = clean_text(data['question'])
                    question = await create_voted_question(
                        self.room, user, question_text)
                else:
                    return # pragma: no cover

            vote_list = []
            question_votes = await database_sync_to_async(question.votes.all)()
            
            for vote in question_votes:
                vote_list.append(encrypt(str(vote.user.id).rjust(10)))
            
            text_question = {
                'id': question.id,
                'question': True,
                'user': encrypt(str(user.id).rjust(10)),
                'groupName': question.room.legislative_body_initials,
                'voteList': vote_list,
                'answered': question.answered,
                'html': question.html_question_body(user, 'room')
            }

            await self.channel_layer.group_send(
                self.group_name,
                {'type': 'room_events',
                 'text': json.dumps(text_question)}
            )

            log.info('Question message is ok.')

        elif set(data.keys()) == set(('handler', 'message')):
            if data['message'].strip():
                message_text = clean_text(data['message'])
                message = await create_chat_message(self.room, user, message_text)
                text_chat = {
                    "chat": True,
                    "html": message.html_body()
                }

                await self.channel_layer.group_send(
                    self.group_name,
                    {'type': 'room_events',
                     'text': json.dumps(text_chat)}
                )
            log.info('Chat message is ok.')

        else:
            log.info("Message unexpected format data") # pragma: no cover
            return # pragma: no cover

    async def room_events(self, event):
        await self.send(text_data=event["text"])
