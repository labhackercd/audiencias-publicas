from channels import Group
from apps.core.models import Room, Question, UpDownVote
from apps.core.utils import decrypt, encrypt
from apps.core.consumers.utils import get_room, get_data
from django.contrib.auth.models import User
from django.conf import settings
import json
import logging
import re

log = logging.getLogger("chat")


def on_connect(message, pk):
    message.reply_channel.send({
        'accept': True
    })
    room = get_room(pk)
    if room is not None:
        Group(room.group_questions_name).add(message.reply_channel)
        log.debug('Questions websocket connected.')


def on_receive(message, pk):
    room = get_room(pk)
    data = get_data(message)

    if room.youtube_status != 2:
        if set(data.keys()) != set(('handler', 'question', 'is_vote')):
            log.debug("Message unexpected format data")
            return
        else:
            log.debug('Question message is ok.')

        if not data['handler']:
            return

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
            blackList = settings.WORDS_BLACK_LIST
            wordList = re.sub("[^\w]", " ", data['question'].lower()).split()
            censured_words = list(set(blackList) & set(wordList))
            query = data['question']

            if censured_words:
                for word in censured_words:
                    query = re.sub(word, '♥', query, flags=re.IGNORECASE)
            question = Question.objects.create(room=room, user=user,
                                               question=query)
            UpDownVote.objects.create(question=question, user=user, vote=True)

        vote_list = []
        for vote in question.votes.all():
            vote_list.append(encrypt(str(vote.user.id).rjust(10)))

        Group(room.group_questions_name).send(
            {'text': json.dumps({
                'id': question.id,
                'user': encrypt(str(user.id).rjust(10)),
                'groupName': question.room.legislative_body_initials,
                'voteList': vote_list,
                'answered': question.answered,
                'html': question.html_question_body(user)
            })}
        )


def on_disconnect(message, pk):
    try:
        room = Room.objects.get(pk=pk)
        Group(room.group_questions_name).discard(message.reply_channel)
        log.debug('Questions websocket disconnected.')
    except (KeyError, Room.DoesNotExist):
        pass
