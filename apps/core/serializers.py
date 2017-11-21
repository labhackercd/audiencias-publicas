from django.conf import settings
from rest_framework import serializers
from apps.core.models import Message, Question, UpDownVote, Room
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'username', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)

        try:
            request = kwargs.get('context').get('request')
            api_key = request.GET.get('api_key', None)

            if api_key != settings.SECRET_KEY:
                self.fields.pop('email')

        except AttributeError:
            pass


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name')


class VoteSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UpDownVote
        fields = ('id', 'user', 'question', 'vote')


class QuestionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    votes = VoteSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'room', 'user', 'question',
                  'created', 'modified', 'votes')


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Message
        fields = ('id', 'room', 'user', 'message', 'created', 'modified')


class RoomSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Room
        fields = ('id', 'cod_reunion', 'online_users', 'youtube_id',
                  'legislative_body_alias', 'legislative_body_initials',
                  'youtube_status', 'is_joint', 'max_online_users', 'created',
                  'modified', 'is_visible', 'reunion_type', 'title_reunion',
                  'reunion_object', 'reunion_theme', 'date',
                  'legislative_body', 'reunion_status', 'location')
