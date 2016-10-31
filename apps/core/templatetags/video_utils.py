from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
import re


register = template.Library()


@register.filter
@stringfilter
def simplify(value):
    replaced = re.sub(' - Audiência Pública .*', '', value)
    return replaced


@register.simple_tag(takes_context=True)
def vote_action(context, question, user):
    if question.user.username == user:
        html = render_to_string('includes/question_action.html', {
            'extra_classes': 'voted disabled',
            'total_votes': question.votes_count,
            'extra_attributes': 'disabled',
            'upvote_content': 'Sua Pergunta'})
    elif question.votes.filter(user__username=user).count() > 0:
        html = render_to_string('includes/question_action.html', {
            'extra_classes': 'voted',
            'question_vote': 'question-vote',
            'total_votes': question.votes_count,
            'upvote_content': 'Apoiada por você'})
    else:
        html = render_to_string('includes/question_action.html', {
            'question_vote': 'question-vote',
            'total_votes': question.votes_count,
            'upvote_content': 'Votar Nesta Pergunta'})
    return mark_safe(html)
