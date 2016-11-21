from channels import Group
from apps.core.models import Video, Question, UpDownVote
from apps.core.utils import decrypt, encrypt
from apps.core.consumers.utils import get_video, get_data
from django.contrib.auth.models import User
from django.conf import settings
import json
import logging
import re

log = logging.getLogger("chat")


def on_connect(message, pk):
    video = get_video(pk)
    if video is not None:
        Group(video.group_questions_name).add(message.reply_channel)
        log.debug('Questions websocket connected.')


def on_receive(message, pk):
    video = get_video(pk)
    data = get_data(message)

    if not video.closed_date:
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
            question = Question.objects.create(video=video, user=user,
                                               question=query)
            UpDownVote.objects.create(question=question, user=user, vote=True)

        vote_list = []
        for vote in question.votes.all():
            vote_list.append(encrypt(str(vote.user.id).rjust(10)))

        Group(video.group_questions_name).send(
            {'text': json.dumps({'id': question.id,
                                 'user': encrypt(str(user.id).rjust(10)),
                                 'voteList': vote_list,
                                 'html': question.html_question_body(user)})}
        )


def on_disconnect(message, pk):
    try:
        video = Video.objects.get(pk=pk)
        Group(video.group_questions_name).discard(message.reply_channel)
        log.debug('Questions websocket disconnected.')
    except (KeyError, Video.DoesNotExist):
        pass
