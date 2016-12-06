from django.contrib.auth.models import User
from rest_framework import serializers
from apps.core.models import Agenda, Message, Question, Video, UpDownVote


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpDownVote
        fields = ('id', 'user', 'question', 'vote')


class AgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agenda
        fields = ('id', 'date', 'session', 'location', 'situation', 'commission')


class QuestionSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'video', 'user', 'question',
                  'created', 'modified', 'votes')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'video', 'user', 'message', 'created', 'modified')


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'videoId', 'thumb_default', 'thumb_medium',
                  'thumb_high', 'title', 'description', 'published_date',
                  'closed_date', 'slug', 'created', 'modified')
