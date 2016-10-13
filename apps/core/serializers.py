from rest_framework import serializers
from apps.core.models import Agenda, Message, Question, Video


class AgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agenda
        fields = ('id', 'date', 'session', 'location', 'situation', 'commission')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('video', 'user', 'question',
                  'timestamp', 'up_votes', 'down_votes')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('video', 'user', 'message', 'timestamp')


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('videoId', 'thumb_default', 'thumb_medium',
                  'thumb_high', 'title', 'description',
                  'published_date', 'closed_date', 'slug')
