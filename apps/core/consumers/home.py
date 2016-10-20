from channels import Group


def connect(message):
    Group('home').add(message.reply_channel)


def disconnect(message):
    Group('home').discard(message.reply_channel)
