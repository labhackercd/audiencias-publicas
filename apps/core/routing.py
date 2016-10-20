from channels import route
from .consumers import home

channel_routing = [
    route("websocket.connect", home.connect),
    route("websocket.disconnect", home.disconnect),
]
