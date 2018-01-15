from django.conf import settings
from rest_framework import serializers
from apps.core.models import Message, Question, UpDownVote, Room
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'username', 'first_name', 'last_name')

    def to_representation(self, instance):
        ret = super(UserSerializer, self).to_representation(instance)
        request = self.context.get('request', None)
        if request:
            api_key = request.GET.get('api_key', None)
            if api_key != settings.SECRET_KEY:
                ret.pop('email')
        else:
            ret.pop('email')
        return ret


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
    class Meta:
        model = Room
        fields = ('id', 'cod_reunion', 'online_users',
                  'legislative_body_alias', 'legislative_body_initials',
                  'youtube_status', 'is_joint', 'max_online_users', 'created',
                  'modified', 'is_visible', 'reunion_type', 'title_reunion',
                  'reunion_object', 'reunion_theme', 'date',
                  'legislative_body', 'reunion_status', 'location')
