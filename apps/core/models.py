# -*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class Video(models.Model):
    videoId = models.CharField(max_length=200)
    thumb_default = models.URLField(null=True, blank=True)
    thumb_medium = models.URLField(null=True, blank=True)
    thumb_high = models.URLField(null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    published_date = models.DateTimeField(auto_now=True)
    closed_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.videoId

    class Meta:
        verbose_name = _('video')
        verbose_name_plural = _('videos')


class Message(models.Model):
    video = models.ForeignKey(Video, related_name='messages')
    handle = models.ForeignKey(settings.AUTH_USER_MODEL)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True, db_index=True)

    def __unicode__(self):
        return self.message

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')
