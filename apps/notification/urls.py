from django.conf.urls import url
from apps.notification.views import send_participants_notification


urlpatterns = [
    url(r'^participants/(?P<room_id>\d+)/?$', send_participants_notification,
        name='participants_notification'),
]
