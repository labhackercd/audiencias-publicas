from django.contrib import admin
from apps.core.models import Agenda, Message, Question, Video


admin.site.register(Agenda)
admin.site.register(Message)
admin.site.register(Question)
admin.site.register(Video)
