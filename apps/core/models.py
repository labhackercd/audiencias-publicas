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
    TYPE_CHOICES = (
        (1, 'Comissão Diretora'),
        (2, 'Comissão Permanente'),
        (3, 'Comissão Especial'),
        (4, 'Comissão Parlamentar de Inquérito'),
        (5, 'Comissão Externa'),
        (6, 'Comissão Mista Permanente'),
        (11, 'Conselho')
    )
    YOUTUBE_STATUS_CHOICES = (
        (0, 'Sem transmissão'),
        (1, 'Em andamento'),
        (2, 'Transmissão encerrada')
    )
    cod_reunion = models.CharField(max_length=200, null=True, blank=True)
    title_reunion = models.CharField(max_length=200, null=True, blank=True)
    legislative_body_initials = models.CharField(max_length=200, null=True,
                                                 blank=True)
    legislative_body_alias = models.CharField(max_length=200, null=True,
                                              blank=True)
    legislative_body = models.TextField(null=True, blank=True)
    subcommission = models.CharField(max_length=200, null=True, blank=True)
    reunion_status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    reunion_type = models.CharField(max_length=200, null=True, blank=True)
    reunion_object = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    legislative_body_type = models.IntegerField(choices=TYPE_CHOICES,
                                                default=1)
    is_joint = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)
    youtube_status = models.IntegerField(choices=YOUTUBE_STATUS_CHOICES,
                                         default=0)
    youtube_id = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    online_users = models.IntegerField(default=0)
    max_online_users = models.IntegerField(default=0)
    is_visible = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('room')
        verbose_name_plural = _('rooms')

    def __str__(self):
        if self.legislative_body_alias:
            return self.legislative_body_alias
        elif self.title_reunion:
            return self.title_reunion
        else:
            return 'object'

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
    question = models.ForeignKey('Question', related_name='votes')
    vote = models.BooleanField(default=False, choices=((True, _('Up Vote')),
                               (False, _('Down Vote'))))

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Message(TimestampedMixin):
    room = models.ForeignKey(Room, related_name='messages', null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    message = models.TextField()

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
    room = models.ForeignKey(Room, related_name='questions', null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    question = models.TextField(max_length='600')
    answer_time = models.IntegerField(null=True, blank=True)

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
    if instance.youtube_status == 2:
        is_closed = True
    instance.send_notification(is_closed=is_closed)


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
models.signals.post_save.connect(room_post_save, sender=Room)
