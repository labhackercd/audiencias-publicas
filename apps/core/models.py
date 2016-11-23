# -*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
import datetime
from django_q.tasks import schedule
from django_q.models import Schedule
from channels import Group
from apps.core.utils import encrypt
# from apps.core.views import notification
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


class UpDownVote(TimestampedMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'))
    question = models.ForeignKey('Question', related_name='votes')
    vote = models.BooleanField(default=False, choices=((True, _('Up Vote')),
                               (False, _('Down Vote'))))

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Video(TimestampedMixin):
    videoId = models.CharField(max_length=200, unique=True)
    thumb_default = models.URLField(null=True, blank=True)
    thumb_medium = models.URLField(null=True, blank=True)
    thumb_high = models.URLField(null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    published_date = models.DateTimeField(auto_now=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(max_length=200, blank=True)

    class Meta:
        verbose_name = _('video')
        verbose_name_plural = _('videos')

    def __str__(self):
        return self.videoId

    @models.permalink
    def get_absolute_url(self):
        return ('video_room', [self.pk])

    def html_body(self):
        return render_to_string('includes/home_video.html', {'video': self})

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


class Message(TimestampedMixin):
    video = models.ForeignKey(Video, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    message = models.TextField()

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')

    def __str__(self):
        return self.message

    def html_body(self):
        return render_to_string('includes/chat_message.html',
                                {'message': self})


class Question(TimestampedMixin):
    video = models.ForeignKey(Video, related_name='questions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    question = models.TextField()
    answer_time = models.CharField(max_length=200, null=True, blank=True)

    @property
    def votes_count(self):
        return self.votes.filter(vote=True).count()

    def html_question_body(self, user):
        return render_to_string(
            'includes/video_questions.html',
            {'question': self,
             'user': user,
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
        Group(self.video.group_room_questions_name).send(
            {'text': json.dumps(text)}
        )

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')

    def __str__(self):
        return self.question


class Agenda(TimestampedMixin):
    date = models.DateTimeField(null=True, blank=True)
    session = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    situation = models.CharField(max_length=200, null=True, blank=True)
    commission = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = _('agenda')
        verbose_name_plural = _('agendas')

    def __str__(self):
        if self.session and self.location:
            return self.session + ', ' + self.location
        else:
            return 'Agenda'

    def is_today(self):
        if datetime.date.today() == self.date.date():
            return True
        return False

    def is_tomorrow(self):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        if self.date.date() == tomorrow:
            return True
        return False


def notification(subject, html, email_list):
    mail = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER,
                                  email_list)
    mail.attach_alternative(html, 'text/html')
    mail.send()


def video_pre_save(signal, instance, sender, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


def video_post_save(sender, instance, created, **kwargs):
    is_closed = False
    if created:
        schedule('apps.core.tasks.close_room', instance.videoId,
                 name=instance.videoId, schedule_type='I')

    if instance.closed_date is not None:
        is_closed = True

    instance.send_notification(is_closed=is_closed)


def video_post_delete(sender, instance, **kwargs):
    instance.send_notification(deleted=True)
    try:
        Schedule.objects.get(name=instance.videoId).delete()
    except Schedule.DoesNotExist:
        pass


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


models.signals.pre_save.connect(video_pre_save, sender=Video)
models.signals.post_save.connect(video_post_save, sender=Video)
models.signals.post_delete.connect(video_post_delete, sender=Video)
models.signals.post_save.connect(vote_post_save, sender=UpDownVote)
models.signals.post_delete.connect(vote_post_delete, sender=UpDownVote)
