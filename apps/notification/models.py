# -*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from apps.core.models import TimestampedMixin, Room


class ParticipantNotification(TimestampedMixin):
    room = models.ForeignKey(Room, verbose_name=_('room'),
                             on_delete=models.CASCADE)
    emails = models.TextField()
    subject = models.CharField(_('subject'), max_length=100)
    content = models.TextField(_('content'))

    class Meta:
        verbose_name = _('participant notification')
        verbose_name_plural = _('participants notifications')

    def __str__(self):
        return self.room.__str__()
