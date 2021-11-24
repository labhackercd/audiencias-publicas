from django.conf import settings
from django.urls import path
from apps.core.consumers import home, room, room_questions

if settings.URL_PREFIX:
    prefix = settings.URL_PREFIX
else:
    prefix = ''

websocket_urlpatterns = [
    path(prefix + 'home/stream/', home.HomeConsumer.as_asgi()),
    path(prefix + 'sala/<int:room_id>/perguntas/stream/',
         room_questions.QuestionsPanelConsumer.as_asgi()),
    path(prefix + 'sala/<int:room_id>/stream/',
         room.RoomConsumer.as_asgi()),
]
