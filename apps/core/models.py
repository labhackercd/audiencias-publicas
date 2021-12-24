from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
import datetime
from apps.core.utils import encrypt
import json
from constance import config
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.urls import reverse

channel_layer = get_channel_layer()


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
    YOUTUBE_STATUS_CHOICES = (
        (0, 'Sem transmissão'),
        (1, 'Em andamento'),
        (2, 'Transmissão encerrada'),
        (3, 'Cancelada')
    )
    cod_reunion = models.CharField(_('code reunion'), max_length=200,
                                   null=True, blank=True)
    title_reunion = models.CharField(_('title reunion'), max_length=200,
                                     null=True, blank=True)
    legislative_body_initials = models.CharField(
        _('legislative body initials'), max_length=200, null=True, blank=True)
    legislative_body = models.TextField(_('legislative body'), null=True,
                                        blank=True)
    reunion_type = models.CharField(_('reunion type'), max_length=200,
                                    null=True, blank=True)
    reunion_object = models.TextField(_('reunion object'), null=True,
                                      blank=True)
    reunion_theme = models.TextField(_('reunion theme'), null=True, blank=True)
    location = models.CharField(_('location'), max_length=200, null=True,
                                blank=True)
    youtube_status = models.IntegerField(_('youtube status'),
                                         choices=YOUTUBE_STATUS_CHOICES,
                                         default=0)
    date = models.DateTimeField(_('date'), null=True, blank=True)
    online_users = models.IntegerField(_('online users'), default=0)
    max_online_users = models.IntegerField(_('max online users'), default=0)
    views = models.IntegerField(_('views'), default=0)
    is_visible = models.BooleanField(_('is visible'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)
    external_link = models.URLField(verbose_name=_('link'), null=True,
                                    blank=True)
    closed_time = models.DateTimeField(_('closed time'), null=True, blank=True)

    class Meta:
        verbose_name = _('room')
        verbose_name_plural = _('rooms')

    def __str__(self):
        if self.title_reunion:
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

    def time_to_close(self):
        if self.closed_time:
            time = self.closed_time + datetime.timedelta(minutes=15)
            time_to_close = time - timezone.now()
            total_seconds = time_to_close.total_seconds()
            if total_seconds >= 0:
                return total_seconds
        return False

    def latest_video(self):
        if self.videos:
            latest = self.videos.filter(is_attachment=False).latest('created')
            return latest
        return False

    def get_main_videos(self):
        return self.videos.filter(is_attachment=False).order_by('-created')

    def get_attachment_videos(self):
        return self.videos.filter(is_attachment=True).order_by('order',
                                                               'created')

    def get_absolute_url(self):
        return reverse('video_room', args=[str(self.id)])

    def html_body(self):
        return render_to_string('includes/home_video.html', {'room': self})

    def html_room_video(self):
        return render_to_string('includes/room_video.html', {'object': self})

    def html_room_thumbnails(self):
        return render_to_string('includes/room_thumbs.html', {'object': self})

    def send_notification(self, deleted=False, is_closed=False):
        notification = {
            'id': self.id,
            'html': self.html_body(),
            'deleted': deleted,
            'is_closed': is_closed
        }
        if is_closed:
            text = {
                'closed': True,
                'time_to_close': self.time_to_close(),
            }
            async_to_sync(channel_layer.group_send)(
                self.group_room_name,
                {'type': 'room_events',
                 'text': json.dumps(text)}
            )
        async_to_sync(channel_layer.group_send)(
            'home',
            {'type': 'home.message',
             'text': json.dumps(notification)}
        )


    @property
    def group_room_name(self):
        return "room-%s" % self.id

    @property
    def group_room_questions_name(self):
        return "video-room-questions-%s" % self.id

    @property
    def questions_count(self):
        return self.questions.count()

    @property
    def messages_count(self):
        return self.messages.count()

    @property
    def votes_count(self):
        return UpDownVote.objects.filter(question__room=self).count()

    @property
    def participants_count(self):
        questions = self.questions.prefetch_related('votes__user')
        vote_users = [user_id for question in questions
            for user_id in question.votes.values_list('user__id', flat=True)]
        question_users = list(questions.values_list('user__id', flat=True))
        message_users = list(
            self.messages.values_list('user__id', flat=True))
        total_users = len(
            list(set(vote_users + question_users + message_users)))
        return total_users


class UpDownVote(TimestampedMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name=_('user'), related_name='votes',)
    question = models.ForeignKey('Question', related_name='votes',
                                 verbose_name=_('question'), on_delete=models.CASCADE)
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
                             verbose_name=_('room'), on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages',
                             verbose_name=_('user'), on_delete=models.CASCADE)
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


class Video(TimestampedMixin):
    room = models.ForeignKey(Room, related_name='videos',
                             verbose_name=_('room'), on_delete=models.CASCADE)
    video_id = models.CharField(_('youtube id'), max_length=200)
    title = models.CharField(_('title'), max_length=200, null=True, blank=True)
    is_attachment = models.BooleanField(_('is_attachment'), default=False)
    order = models.IntegerField(_('order'), default=0)

    class Meta:
        verbose_name = _('video')
        verbose_name_plural = _('videos')

    def __str__(self):
        return self.video_id

    def send_video(self):
        text = {
            'video': True,
            'is_attachment': self.is_attachment,
            'video_id': self.video_id,
            'video_html': self.room.html_room_video(),
            'thumbs_html': self.room.html_room_thumbnails(),
        }
        async_to_sync(channel_layer.group_send)(
            self.room.group_room_name,
            {'type': 'room_events',
             'text': json.dumps(text)}
        )


class Question(TimestampedMixin):
    room = models.ForeignKey(Room, related_name='questions', null=True,
                             verbose_name=_('room'), on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name=_('user'), related_name='questions')
    question = models.TextField(_('question'), max_length=300)
    video = models.ForeignKey(Video, verbose_name=_('video'), null=True,
                              related_name='questions',
                              on_delete=models.SET_NULL)
    answer_time = models.CharField(_('answer time'), max_length=200,
                                   null=True, blank=True)
    answered = models.BooleanField(_('answered'), default=False)
    is_priority = models.BooleanField(_('is priority'), default=False)

    @property
    def votes_count(self):
        return self.votes.filter(vote=True).count()

    def html_question_body(self, user, page=None):
        return render_to_string(
            'includes/question_card.html',
            {'question': self,
             'user': user,
             'page': page,
             'author': encrypt(str(self.user.id).rjust(10))}
        )

    def send_notification(self, user):
        html = self.html_question_body(
            user, 'question-panel')
        text = {
            'html': html,
            'counter': self.room.questions.count(),
            'id': self.id
        }
        async_to_sync(channel_layer.group_send)(
            self.room.group_room_questions_name,
            {'type': 'questions_panel',
             'text': json.dumps(text)}
        )

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')

    def __str__(self):
        return self.question


class RoomAttachment(TimestampedMixin):
    room = models.ForeignKey(Room, related_name='attachments',
                             verbose_name=_('room'), on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=200, null=True, blank=True)
    url = models.URLField(verbose_name=_('link'))

    class Meta:
        verbose_name = _('attachment')
        verbose_name_plural = _('attachments')

    def __str__(self):
        return self.room.__str__()


def room_post_save(sender, instance, created, **kwargs):
    is_closed = False
    user_message = config.WELCOME_MESSAGE_USER_ID
    message = config.WELCOME_MESSAGE
    video = config.WELCOME_VIDEO
    video_title = config.WELCOME_VIDEO_TITLE

    if created and video != '':
        Video.objects.create(room=instance,
                             video_id=video,
                             title=video_title,
                             is_attachment=True)
    if created and user_message != 0 and message != '':
        Message.objects.create(room=instance,
                               user_id=user_message,
                               message=message)
    if instance.youtube_status in [2, 3]:
        is_closed = True
        if not instance.closed_time:
            instance.closed_time = timezone.now()
            instance.save()
    instance.send_notification(is_closed=is_closed)


def video_post_save(sender, instance, **kwargs):
    notification = {
        'id': instance.room.id,
        'html': instance.room.html_body(),
    }
    instance.send_video()
    if not instance.is_attachment:
        async_to_sync(channel_layer.group_send)(
            'home',
            {'type': 'home.message',
             'text': json.dumps(notification)}
        )


def video_post_delete(sender, instance, **kwargs):
    text = {
        'video': True,
        'deleted': True,
        'thumbs_html': instance.room.html_room_thumbnails(),
    }
    async_to_sync(channel_layer.group_send)(
        instance.room.group_room_name,
        {'type': 'room_events',
         'text': json.dumps(text)}
    )


def vote_post_save(sender, instance, **kwargs):
    instance.question.send_notification(instance.user)


def vote_post_delete(sender, instance, **kwargs):
    instance.question.send_notification(instance.user)


def question_post_save(sender, instance, **kwargs):
    instance.send_notification(instance.user)


models.signals.post_save.connect(question_post_save, sender=Question)
models.signals.post_save.connect(vote_post_save, sender=UpDownVote)
models.signals.post_delete.connect(vote_post_delete, sender=UpDownVote)
models.signals.post_save.connect(room_post_save, sender=Room)
models.signals.post_save.connect(video_post_save, sender=Video)
models.signals.post_delete.connect(video_post_delete, sender=Video)
