import json
import logging
import re
from apps.core.models import Message, Question, UpDownVote
from apps.core.utils import decrypt, encrypt
from apps.core.consumers.utils import get_room, get_data
from constance import config
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

User = get_user_model()
log = logging.getLogger('ws-logger')


class RoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        room_id = self.scope['url_route']['kwargs']['room_id']
        room = get_room(room_id)
        self.group_name = room.group_room_name

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        if room is not None:
            room.online_users += 1
            room.views += 1

            if room.online_users > room.max_online_users:
                room.max_online_users = room.online_users

            async_save = sync_to_async(room.save)
            await async_save()

            log.info('Room websocket connected.')
    
    async def receive(self, text_data=None, bytes_data=None):
        room_id = self.scope['url_route']['kwargs']['room_id']
        room = get_room(room_id)
        data = get_data(text_data)

        if not 'handler' in data.keys():
            log.info('Connected as annonymous user.')
            return

        blackList = [x.strip() for x in config.WORDS_BLACK_LIST.split(',')]

        if set(data.keys()) == set(('handler', 'question', 'is_vote')):
            user = User.objects.get(id=decrypt(data['handler']))
            
            if data['is_vote']:
                question = Question.objects.get(id=data['question'])
                
                if question.user != user:
                    vote, created = UpDownVote.objects.get_or_create(
                        user=user, question=question, vote=True
                    )

                    if not created:
                        vote.delete()

            else:
                if len(data['question']) <= 300:
                    wordList = re.sub(
                        "[^\w]", " ", data['question'].lower()).split()
                    censured_words = list(set(blackList) & set(wordList))
                    query = data['question']

                    if censured_words:
                        for word in censured_words:
                            query = re.sub(word, '♥', query, flags=re.IGNORECASE)
                    
                    question = Question.objects.create(
                        room=room, user=user, question=query)
                    UpDownVote.objects.create(
                        question=question, user=user, vote=True)

                else:
                    return

            vote_list = []

            for vote in question.votes.all():
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
            word_list = re.sub("[^\w]", " ", data['message'].lower()).split()
            censured_words = list(set(blackList) & set(word_list))
            message = data['message']

            if message.strip():
                if censured_words:
                    for word in censured_words:
                        message = re.sub(word, '♥', message, flags=re.IGNORECASE)
                user = User.objects.get(id=decrypt(data['handler']))
                message = Message.objects.create(
                    room=room, user=user, message=message)
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
            log.info("Message unexpected format data")
            return

    async def disconnect(self, close_code):
        room_id = self.scope['url_route']['kwargs']['room_id']
        room = get_room(room_id)
        room.online_users -= 1
        room.save()

        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        log.info('Room websocket disconnected. Code: %s' % close_code)
    
    async def room_events(self, event):
        await self.send(text_data=event["text"])
