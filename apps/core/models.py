# -*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.template.defaultfilters import slugify


class Video(models.Model):
    videoId = models.CharField(max_length=200)
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


class Message(models.Model):
    video = models.ForeignKey(Video, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')

    def __unicode__(self):
        return self.message


class Question(models.Model):
    video = models.ForeignKey(Video, related_name='questions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    question = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now=True, db_index=True)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)

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


models.signals.pre_save.connect(video_pre_save, sender=Video)
