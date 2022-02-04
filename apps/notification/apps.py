from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NotificationConfig(AppConfig):
    name = 'apps.notification'
    verbose_name = _('Notification')
