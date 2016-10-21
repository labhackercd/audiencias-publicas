from channels import route
from .consumers import home, chat

channel_routing = [
    route("websocket.connect", home.connect, path=r'^/$'),
    route("websocket.disconnect", home.disconnect, path=r'^/$'),
    route("websocket.connect", chat.connect_room, path=r'^/salas/(?P<pk>\d+)/stream/$'),
    route("websocket.receive", chat.receive_room, path=r'^/salas/(?P<pk>\d+)/stream/$'),
    route("websocket.disconnect", chat.disconnect_room, path=r'^/salas/(?P<pk>\d+)/stream/$'),
]
