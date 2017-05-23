# -*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
import datetime
from channels import Group
from apps.core.utils import encrypt
import json


class TimestampedMixin(models.Model):
    created = models.DateTimeField(_('created'), editable=False,
                                   blank=True, auto_now_add=True)
    modified = models.DateTimeField(_('modified'), editable=False,
                                    blank=True, auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(TimestampedMixin, self).save(*args, **kwargs)


class Room(TimestampedMixin):
    STATUS_CHOICES = (
        (1, 'Não Confirmada'),
        (2, 'Convocada'),
        (3, 'Em Andamento'),
        (4, 'Encerrada'),
        (5, 'Cancelada'),
        (6, 'Suspensa'),
        (7, 'Encerrada (Termo)'),
        (8, 'Encerrada (Final)'),
        (9, 'Encerrada(Comunicado)')
    )
    YOUTUBE_STATUS_CHOICES = (
        (0, 'Sem transmissão'),
        (1, 'Em andamento'),
        (2, 'Transmissão encerrada')
    )
    cod_reunion = models.CharField(_('code reunion'), max_length=200,
                                   null=True, blank=True)
    title_reunion = models.CharField(_('title reunion'), max_length=200,
                                     null=True, blank=True)
    legislative_body_initials = models.CharField(_('legislative body initials'),
                                                 max_length=200, null=True,
                                                 blank=True)
    legislative_body_alias = models.CharField(_('legislative body alias'),
                                              max_length=200, null=True,
                                              blank=True)
    legislative_body = models.TextField(_('legislative body'), null=True,
                                        blank=True)
    reunion_status = models.IntegerField(_('reunion status'),
                                         choices=STATUS_CHOICES, default=1)
    reunion_type = models.CharField(_('reunion type'), max_length=200,
                                    null=True, blank=True)
    reunion_object = models.TextField(_('reunion object'), null=True,
                                      blank=True)
    reunion_theme = models.TextField(_('reunion theme'), null=True, blank=True)
    location = models.CharField(_('location'), max_length=200, null=True,
                                blank=True)
    is_joint = models.BooleanField(_('is joint'), default=False)
    youtube_status = models.IntegerField(_('youtube status'),
                                         choices=YOUTUBE_STATUS_CHOICES,
                                         default=0)
    youtube_id = models.CharField(_('youtube id'), max_length=200, null=True,
                                  blank=True)
    date = models.DateTimeField(_('date'), null=True, blank=True)
    online_users = models.IntegerField(_('online users'), default=0)
    max_online_users = models.IntegerField(_('max online users'), default=0)
    views = models.IntegerField(_('views'), default=0)
    is_visible = models.BooleanField(_('is visible'), default=False)

    class Meta:
        verbose_name = _('room')
        verbose_name_plural = _('rooms')

    def __str__(self):
        if self.legislative_body_alias:
            return self.legislative_body_alias
        elif self.title_reunion:
            return self.title_reunion
        else:
            return _('room')

    def is_today(self):
        if datetime.date.today() == self.date.date():
            return True
        return False

    def is_tomorrow(self):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        if self.date.date() == tomorrow:
            return True
        return False

    def get_absolute_url(self):
        return "%s/sala/%i" % (settings.FORCE_SCRIPT_NAME, self.pk)

    def html_body(self):
        return render_to_string('includes/home_video.html', {'room': self})

    def send_notification(self, deleted=False, is_closed=False):
        notification = {
            'id': self.id,
            'html': self.html_body(),
            'deleted': deleted,
            'is_closed': is_closed
        }
        if is_closed:
            Group(self.group_questions_name).send({'text': 'closed'})
            Group(self.group_chat_name).send({'text': 'closed'})
        Group('home').send({'text': json.dumps(notification)})

    @property
    def group_chat_name(self):
        return "video-chat-%s" % self.id

    @property
    def group_questions_name(self):
        return "video-questions-%s" % self.id

    @property
    def group_room_questions_name(self):
        return "video-room-questions-%s" % self.id


class UpDownVote(TimestampedMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'))
    question = models.ForeignKey('Question', related_name='votes',
                                 verbose_name=_('question'))
    vote = models.BooleanField(_('vote'), default=False,
                               choices=((True, _('Up Vote')),
                               (False, _('Down Vote'))))

    class Meta:
        verbose_name = _('vote')
        verbose_name_plural = _('votes')
        unique_together = ('user', 'question')

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Message(TimestampedMixin):
    room = models.ForeignKey(Room, related_name='messages', null=True,
                             verbose_name=_('room'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_('user'))
    message = models.TextField(_('message'))

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')
        ordering = ['created']

    def __str__(self):
        return self.message

    def html_body(self):
        return render_to_string('includes/chat_message.html',
                                {'message': self})


class Question(TimestampedMixin):
    room = models.ForeignKey(Room, related_name='questions', null=True,
                             verbose_name=_('room'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'))
    question = models.TextField(_('question'), max_length='600')
    answer_time = models.IntegerField(_('answer time'), null=True, blank=True)
    answered = models.BooleanField(_('answered'), default=False)

    @property
    def votes_count(self):
        return self.votes.filter(vote=True).count()

    def html_question_body(self, user):
        return render_to_string(
            'includes/video_questions.html',
            {'question': self,
             'user': user,
             'object': self.room,
             'author': encrypt(str(self.user.id).rjust(10))}
        )

    def html_room_question_body(self):
        return render_to_string('includes/room_question.html',
                                {'question': self})

    def send_notification(self):
        text = {
            'html': self.html_room_question_body(),
            'id': self.id,
        }
        Group(self.room.group_room_questions_name).send(
            {'text': json.dumps(text)}
        )

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')

    def __str__(self):
        return self.question


def notification(subject, html, email_list):
    mail = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER,
                                  email_list)
    mail.attach_alternative(html, 'text/html')
    mail.send()


def room_post_save(sender, instance, created, **kwargs):
    is_closed = False
    if instance.youtube_status in [2, 3]:
        is_closed = True
    instance.send_notification(is_closed=is_closed)


def room_pre_save(sender, instance, **kwargs):
    if instance.reunion_object:
        lines = instance.reunion_object.splitlines()
        lines = list(filter(str.strip, lines))
        for i, line in enumerate(lines):
            if line == 'TEMA':
                theme = lines[i + 1]
                if theme[0] == '"' and theme[-1] == '"':
                    theme = theme[1:-1]
                instance.reunion_theme = theme
            if 'Tema:' in line:
                instance.reunion_theme = line.replace('Tema:', '')


def room_pre_delete(sender, instance, **kwargs):
    if hasattr(instance, 'room'):
        instance.send_notification(deleted=True)


def vote_post_save(sender, instance, **kwargs):
    count_votes = UpDownVote.objects.filter(question=instance.question).count()
    if count_votes == settings.QUESTION_MIN_UPVOTES:
        html = render_to_string('notifications/question.html',
                                {'question': instance.question})
        subject = u'[Audiências] Notificação de pergunta em destaque'
        email_list = []
        notification(subject, html, email_list)

    instance.question.send_notification()


def vote_post_delete(sender, instance, **kwargs):
    instance.question.send_notification()


models.signals.post_save.connect(vote_post_save, sender=UpDownVote)
models.signals.post_delete.connect(vote_post_delete, sender=UpDownVote)
models.signals.pre_save.connect(room_pre_save, sender=Room)
models.signals.post_save.connect(room_post_save, sender=Room)
