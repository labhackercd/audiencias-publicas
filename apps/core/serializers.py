from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import serializers
from apps.core.models import Agenda, Message, Question, Video, UpDownVote, Room


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpDownVote
        fields = ('id', 'user', 'question', 'vote')


class AgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agenda
        fields = ('id', 'date', 'session', 'location', 'situation',
                  'commission', 'created', 'modified')


class QuestionSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer()
    votes = VoteSerializer(many=True)

    def __init__(self, *args, **kwargs):
        super(QuestionSerializer, self).__init__(*args, **kwargs)

        try:
            request = kwargs.get('context').get('request')
            api_key = request.GET.get('api_key', None)

            if api_key and api_key == settings.SECRET_KEY:
                self.fields['user'] = UserSerializer()
            else:
                self.fields['user'] = BasicUserSerializer()
        except AttributeError:
            # When django initializes kwarg is None
            pass

    class Meta:
        model = Question
        fields = ('id', 'room', 'user', 'question',
                  'created', 'modified', 'votes')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'room', 'user', 'message', 'created', 'modified')


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'videoId', 'thumb_default', 'thumb_medium',
                  'thumb_high', 'title', 'description', 'published_date',
                  'closed_date', 'slug', 'created', 'modified', 'online_users',
                  'max_online_users')


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'agenda', 'video', 'cod_reunion', 'online_users',
                  'max_online_users')
