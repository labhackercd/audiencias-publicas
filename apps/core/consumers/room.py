import json
import logging
import re
from channels import Group
from apps.core.models import Room, Message, Question, UpDownVote
from apps.core.utils import decrypt, encrypt
from apps.core.consumers.utils import get_room, get_data
from constance import config
from channels_presence.models import Room as RoomPresence, Presence
from channels.auth import channel_session_user, channel_session_user_from_http
from channels_presence.decorators import touch_presence, remove_presence
from django.contrib.auth import get_user_model
User = get_user_model()

log = logging.getLogger("room")


@channel_session_user_from_http
def on_connect(message, pk):
    message.reply_channel.send({
        'accept': True
    })
    room = get_room(pk)
    if room is not None:
        room_presence = RoomPresence.objects.add(room.group_room_name,
                                                 message.reply_channel.name,
                                                 message.user)
        anonymous_count = room_presence.get_anonymous_count()
        users_count = room_presence.get_users().count()
        room.online_users = anonymous_count + users_count
        room.views += 1
        if room.online_users > room.max_online_users:
            room.max_online_users = room.online_users
        room.save()
        Group(room.group_room_name).add(message.reply_channel)
        log.debug('Room websocket connected.')


@touch_presence
@channel_session_user
def on_receive(message, pk):
    room = get_room(pk)
    data = get_data(message)

    if 'heartbeat' in data.keys():
        Presence.objects.touch(message.reply_channel.name)
        return

    if not data['handler']:
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
                question = Question.objects.create(room=room, user=user,
                                                   question=query)
                UpDownVote.objects.create(
                    question=question, user=user, vote=True)
            else:
                return

        vote_list = []
        for vote in question.votes.all():
            vote_list.append(encrypt(str(vote.user.id).rjust(10)))

        Group(room.group_room_name).send(
            {'text': json.dumps({
                'id': question.id,
                'question': True,
                'user': encrypt(str(user.id).rjust(10)),
                'groupName': question.room.legislative_body_initials,
                'voteList': vote_list,
                'answered': question.answered,
                'html': question.html_question_body(user, 'room')
            })}
        )

        log.debug('Question message is ok.')

    elif set(data.keys()) == set(('handler', 'message')):
        word_list = re.sub("[^\w]", " ", data['message'].lower()).split()
        censured_words = list(set(blackList) & set(word_list))

        message = data['message']

        if message.strip():
            if censured_words:
                for word in censured_words:
                    message = re.sub(word, '♥', message, flags=re.IGNORECASE)

            user = User.objects.get(id=decrypt(data['handler']))
            message = Message.objects.create(room=room, user=user,
                                             message=message)
            Group(room.group_room_name).send(
                {'text': json.dumps({
                    "chat": True,
                    "html": message.html_body()
                })}
            )

        log.debug('Chat message is ok.')

    else:
        log.debug("Message unexpected format data")
        return


@remove_presence
def on_disconnect(message, pk):
    try:
        room = Room.objects.get(pk=pk)
        room.online_users -= 1
        room.save()
        Group(room.group_room_name).discard(message.reply_channel)
        log.debug('Room websocket disconnected.')
    except (KeyError, Room.DoesNotExist):
        pass
