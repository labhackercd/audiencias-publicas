from django.conf import settings
from django.urls import re_path, path
# from apps.core.consumers import home, room, room_questions
from apps.core.consumers import home

if settings.URL_PREFIX:
    prefix = settings.URL_PREFIX
else:
    prefix = ''

websocket_urlpatterns = [
    path(prefix + 'home/stream/', home.HomeConsumer.as_asgi()),
] 

#     route("websocket.connect", room.on_connect,
#           path=prefix + r'/sala/(?P<pk>\d+)/stream/$'),
#     route("websocket.receive", room.on_receive,
#           path=prefix + r'/sala/(?P<pk>\d+)/stream/$'),
#     route("websocket.disconnect", room.on_disconnect,
#           path=prefix + r'/sala/(?P<pk>\d+)/stream/$'),

#     route("websocket.connect", room_questions.on_connect,
#           path=prefix + r'/sala/(?P<pk>\d+)/perguntas/questions-panel/stream/$'),
#     route("websocket.disconnect", room_questions.on_disconnect,
#           path=prefix + r'/sala/(?P<pk>\d+)/perguntas/questions-panel/stream/$'),
