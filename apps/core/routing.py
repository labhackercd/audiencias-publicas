from django.conf import settings
from channels import route
from .consumers import home, chat, questions, room_questions

if settings.URL_PREFIX:
    prefix = r'^/%s' % (settings.URL_PREFIX)
else:
    prefix = r'^'

channel_routing = [
    route("websocket.connect", home.on_connect, path=prefix + r'/$'),
    route("websocket.disconnect", home.on_disconnect, path=prefix + r'/$'),

    route("websocket.connect", chat.on_connect,
          path=prefix + r'/sala/(?P<pk>\d+)/chat/stream/$'),
    route("websocket.receive", chat.on_receive,
          path=prefix + r'/sala/(?P<pk>\d+)/chat/stream/$'),
    route("websocket.disconnect", chat.on_disconnect,
          path=prefix + r'/sala/(?P<pk>\d+)/chat/stream/$'),

    route("websocket.connect", questions.on_connect,
          path=prefix + r'/sala/(?P<pk>\d+)/questions/stream/$'),
    route("websocket.receive", questions.on_receive,
          path=prefix + r'/sala/(?P<pk>\d+)/questions/stream/$'),
    route("websocket.disconnect", questions.on_disconnect,
          path=prefix + r'/sala/(?P<pk>\d+)/questions/stream/$'),

    route("websocket.connect", room_questions.on_connect,
          path=prefix + r'/sala/(?P<pk>\d+)/perguntas/questions/stream/$'),
    route("websocket.disconnect", room_questions.on_disconnect,
          path=prefix + r'/sala/(?P<pk>\d+)/perguntas/questions/stream/$'),
]
