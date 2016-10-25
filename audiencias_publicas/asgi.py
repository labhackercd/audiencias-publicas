import os
import channels.asgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "audiencias_publicas.settings")
channel_layer = channels.asgi.get_channel_layer()
