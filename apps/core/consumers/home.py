from channels import Group
import json


def on_connect(message):
    message.reply_channel.send({"text": json.dumps({"accept": True})})
    Group('home').add(message.reply_channel)


def on_disconnect(message):
    Group('home').discard(message.reply_channel)
