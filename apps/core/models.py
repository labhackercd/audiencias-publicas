# -*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.contenttypes import fields
from django.template.loader import render_to_string
from django.utils import timezone
from django_q.tasks import schedule
from django_q.models import Schedule
from channels import Group
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
    object_pk = models.PositiveIntegerField()
    content_type = models.ForeignKey('contenttypes.ContentType')
    vote = models.BooleanField(default=False, choices=((True, _('Up Vote')),
                               (False, _('Down Vote'))))

    class Meta:
        unique_together = ('user', 'object_pk', 'content_type')

    def __unicode__(self):
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

    def __unicode__(self):
        return self.videoId

    @models.permalink
    def get_absolute_url(self):
        return ('video_room', [self.slug, self.pk])

    def html_body(self):
        return render_to_string('includes/home_video.html', {'video': self})

    def send_notification(self, deleted=False, is_closed=False):
        notification = {
            'id': self.id,
            'html': self.html_body(),
            'deleted': deleted,
            'is_closed': is_closed
        }
        Group('home').send({'text': json.dumps(notification)})


class Message(TimestampedMixin):
    video = models.ForeignKey(Video, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    message = models.TextField()

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')

    def __unicode__(self):
        return self.message


class Question(TimestampedMixin):
    video = models.ForeignKey(Video, related_name='questions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    question = models.CharField(max_length=200)
    votes = fields.GenericRelation(UpDownVote, object_id_field="object_pk")

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')

    def __unicode__(self):
        return self.question


class Agenda(models.Model):
    date = models.DateTimeField(null=True, blank=True)
    session = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    situation = models.CharField(max_length=200, null=True, blank=True)
    commission = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = _('agenda')
        verbose_name_plural = _('agendas')

    def __unicode__(self):
        if self.session and self.location:
            return self.session + ', ' + self.location
        else:
            return 'Agenda'


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
    Schedule.objects.get(name=instance.videoId).delete()


models.signals.pre_save.connect(video_pre_save, sender=Video)
models.signals.post_save.connect(video_post_save, sender=Video)
models.signals.post_delete.connect(video_post_delete, sender=Video)
