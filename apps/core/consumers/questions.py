from channels import Group
from apps.core.models import Video, Question, UpDownVote
from apps.core.utils import decrypt, encrypt
from apps.core.consumers.utils import get_video, get_data
from django.contrib.auth.models import User
import json
import logging

log = logging.getLogger("chat")


def on_connect(message, pk):
    video = get_video(pk)
    if video is not None:
        Group(video.group_questions_name).add(message.reply_channel)
        log.debug('Questions websocket connected.')


def on_receive(message, pk):
    video = get_video(pk)
    data = get_data(message)

    if set(data.keys()) != set(('handler', 'question', 'is_vote')):
        log.debug("Message unexpected format data")
        return
    else:
        log.debug('Question message is ok.')

    user = User.objects.get(id=decrypt(data['handler']))
    if data['is_vote']:
        question = Question.objects.get(id=data['question'])
        vote, created = UpDownVote.objects.get_or_create(
            user=user, question=question, vote=True
        )
        if not created:
            vote.delete()
    else:
        question = Question.objects.create(video=video, user=user,
                                           question=data['question'])
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
