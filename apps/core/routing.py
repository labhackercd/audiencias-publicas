from django.conf import settings
from channels import route
from .consumers import home, room, room_questions

if settings.URL_PREFIX:
    prefix = r'^/%s' % (settings.URL_PREFIX)
else:
    prefix = r'^'

channel_routing = [
    route("websocket.connect", home.on_connect, path=prefix + r'/$'),
    route("websocket.disconnect", home.on_disconnect, path=prefix + r'/$'),

    route("websocket.connect", room.on_connect,
          path=prefix + r'/sala/(?P<pk>\d+)/stream/$'),
    route("websocket.receive", room.on_receive,
          path=prefix + r'/sala/(?P<pk>\d+)/stream/$'),
    route("websocket.disconnect", room.on_disconnect,
          path=prefix + r'/sala/(?P<pk>\d+)/stream/$'),

    route("websocket.connect", room_questions.on_connect,
          path=prefix + r'/sala/(?P<pk>\d+)/perguntas/questions-panel/stream/$'),
    route("websocket.disconnect", room_questions.on_disconnect,
          path=prefix + r'/sala/(?P<pk>\d+)/perguntas/questions-panel/stream/$'),
]
