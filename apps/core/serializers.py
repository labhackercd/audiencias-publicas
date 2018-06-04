from django.conf import settings
from rest_framework import serializers
from apps.core.models import Message, Question, UpDownVote, Room, Video
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_active', 'is_staff', 'is_superuser')

    def to_representation(self, instance):
        ret = super(UserSerializer, self).to_representation(instance)
        request = self.context.get('request', None)
        if request:
            api_key = request.GET.get('api_key', None)
            if api_key != settings.SECRET_KEY:
                ret.pop('email')
        else:
            ret.pop('email')

        ret.pop('is_active', None)
        ret.pop('is_staff', None)
        ret.pop('is_superuser', None)

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


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'video_id', 'title', 'is_attachment', 'order')


class RoomSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()
    messages_count = serializers.SerializerMethodField()
    youtube_id = serializers.SerializerMethodField()
    videos = VideoSerializer(many=True)

    class Meta:
        model = Room
        fields = ('id', 'cod_reunion', 'online_users',
                  'legislative_body_initials', 'youtube_status',
                  'max_online_users', 'created', 'modified', 'is_visible',
                  'reunion_type', 'title_reunion', 'reunion_object',
                  'reunion_theme', 'date', 'legislative_body', 'location',
                  'questions_count', 'messages_count', 'videos', 'youtube_id')

    def get_questions_count(self, obj):
        return obj.questions.count()

    def get_messages_count(self, obj):
        return obj.messages.count()

    def get_youtube_id(self, obj):
        try:
            return obj.latest_video().video_id
        except Video.DoesNotExist:
            return None
