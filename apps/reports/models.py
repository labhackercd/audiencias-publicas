# -*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from apps.core.models import TimestampedMixin


PERIOD_CHOICES = (
    ('daily', _('Daily')),
    ('monthly', _('Monthly')),
    ('yearly', _('Yearly')),
    ('all', _('All the time')),
)


class AnalysisMixin(TimestampedMixin):
    start_date = models.DateField(_('start date'), db_index=True)
    end_date = models.DateField(_('end date'), db_index=True)
    period = models.CharField(_('period'), max_length=200, db_index=True,
                              choices=PERIOD_CHOICES, default='daily')

    class Meta:
        abstract = True


class NewUsers(AnalysisMixin):
    new_users = models.IntegerField(_('new users'), null=True, blank=True,
                                    default=0)
    class Meta:
        verbose_name = _('new user')
        verbose_name_plural = _('new users')
        unique_together = ('start_date', 'period')

    def __str__(self):
        return ('{} - {}').format(
            self.start_date.strftime("%d/%m/%Y"), self.period)


class VotesReport(AnalysisMixin):
    votes = models.IntegerField(_('votes'), null=True, blank=True,
                                default=0)
    class Meta:
        verbose_name = _('vote')
        verbose_name_plural = _('votes')
        unique_together = ('start_date', 'period')

    def __str__(self):
        return ('{} - {}').format(
            self.start_date.strftime("%d/%m/%Y"), self.period)


class RoomsReport(AnalysisMixin):
    finished_rooms = models.IntegerField(_('finished rooms'), null=True,
                                         blank=True, default=0)
    canceled_rooms = models.IntegerField(_('canceled rooms'), null=True,
                                         blank=True, default=0)
    total_rooms = models.IntegerField(_('total rooms'), null=True, blank=True,
                                      default=0)
    class Meta:
        verbose_name = _('room')
        verbose_name_plural = _('rooms')
        unique_together = ('start_date', 'period')

    def __str__(self):
        return ('{} - {}').format(
            self.start_date.strftime("%d/%m/%Y"), self.period)


class QuestionsReport(AnalysisMixin):
    questions = models.IntegerField(_('questions'), null=True, blank=True,
                                default=0)
    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')
        unique_together = ('start_date', 'period')

    def __str__(self):
        return ('{} - {}').format(
            self.start_date.strftime("%d/%m/%Y"), self.period)


class MessagesReport(AnalysisMixin):
    messages = models.IntegerField(_('messages'), null=True, blank=True,
                                   default=0)
    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')
        unique_together = ('start_date', 'period')

    def __str__(self):
        return ('{} - {}').format(
            self.start_date.strftime("%d/%m/%Y"), self.period)


class ParticipantsReport(AnalysisMixin):
    participants = models.IntegerField(_('participants'), null=True,
                                       blank=True, default=0)

    class Meta:
        verbose_name = _('participant')
        verbose_name_plural = _('participants')
        unique_together = ('start_date', 'period')

    def __str__(self):
        return ('{} - {}').format(
            self.start_date.strftime("%d/%m/%Y"), self.period)
