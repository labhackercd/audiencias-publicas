from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib.auth.models import Group
import datetime
import re


register = template.Library()


@register.filter
@stringfilter
def simplify(value):
    replaced = re.sub(' - Audiência Pública .*', '', value)
    return replaced


@register.simple_tag()
def vote_action(question, user):
    if question.answered:
        html = render_to_string('includes/question_action.html', {
            'extra_classes': 'voted disabled',
            'total_votes': question.votes_count,
            'extra_attributes': 'disabled',
            'room': question.room,
            'upvote_content': 'Pergunta Respondida'})
    elif question.room.youtube_status == 2:
        html = render_to_string('includes/question_action.html', {
            'extra_classes': 'disabled',
            'total_votes': question.votes_count,
            'extra_attributes': 'disabled',
            'room': question.room,
            'upvote_content': 'Votação Encerrada'})
    elif question.user.username == user:
        html = render_to_string('includes/question_action.html', {
            'extra_classes': 'voted disabled',
            'total_votes': question.votes_count,
            'extra_attributes': 'disabled',
            'room': question.room,
            'upvote_content': 'Sua Pergunta'})
    elif question.votes.filter(user__username=user).count() > 0:
        html = render_to_string('includes/question_action.html', {
            'extra_classes': 'voted',
            'question_vote': 'question-vote',
            'total_votes': question.votes_count,
            'room': question.room,
            'upvote_content': 'Apoiada por você'})
    else:
        html = render_to_string('includes/question_action.html', {
            'question_vote': 'question-vote',
            'total_votes': question.votes_count,
            'room': question.room,
            'upvote_content': 'Votar Nesta Pergunta'})
    return mark_safe(html)


@register.filter()
def format_seconds(s):
    if s:
        return str(datetime.timedelta(seconds=float(s))).split('.')[0]


@register.filter()
def belongs_to_group(user, group_name):
    if hasattr(user, 'profile'):
        user_is_admin = user.profile.is_admin
    else:
        user_is_admin = False

    try:
        group = Group.objects.get(name=group_name)
        return group in user.groups.all() or user_is_admin
    except Group.DoesNotExist:
        return False or user_is_admin
