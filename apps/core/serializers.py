from django.conf import settings
from rest_framework import serializers
from apps.core.models import Message, Question, UpDownVote, Room, Video
from django.contrib.auth import get_user_model
from django.db.models import Count, Sum


class UserSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()
    messages_count = serializers.SerializerMethodField()
    votes_count = serializers.SerializerMethodField()
    participations_count = serializers.SerializerMethodField()
    questions_votes_count = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_active', 'is_staff', 'is_superuser', 'questions_count',
                  'messages_count', 'votes_count', 'participations_count',
                  'questions_votes_count', 'date_joined', 'last_login')


    def get_questions_count(self, obj):
        return obj.questions.count()

    def get_messages_count(self, obj):
        return obj.messages.count()

    def get_votes_count(self, obj):
        return obj.votes.count()

    def get_participations_count(self, obj):
        return obj.questions.count() + obj.messages.count() + obj.votes.count()

    def get_questions_votes_count(self, obj):
        questions = obj.questions.annotate(total_votes=Count('votes'))
        votes_count = questions.aggregate(Sum('total_votes'))[
            'total_votes__sum'] or 0
        return votes_count

    def to_representation(self, instance):
        ret = super(UserSerializer, self).to_representation(instance)
        request = self.context.get('request', None)
        if request:
            api_key = request.GET.get('api_key', None)
            if api_key != settings.SECRET_KEY:
                ret.pop('email')
        else:
            ret.pop('email') # pragma: no cover

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
    messages_count = serializers.ReadOnlyField()
    questions_count = serializers.ReadOnlyField()
    votes_count = serializers.ReadOnlyField()
    participants_count = serializers.ReadOnlyField()
    answered_questions_count = serializers.SerializerMethodField()
    youtube_id = serializers.SerializerMethodField()
    videos = VideoSerializer(many=True)

    class Meta:
        model = Room
        fields = ('id', 'cod_reunion', 'online_users',
                  'legislative_body_initials', 'youtube_status',
                  'max_online_users', 'created', 'modified', 'is_visible',
                  'reunion_type', 'title_reunion', 'reunion_object',
                  'reunion_theme', 'date', 'legislative_body', 'location',
                  'questions_count', 'answered_questions_count', 'messages_count',
                  'votes_count', 'participants_count', 'videos', 'youtube_id')

    def get_answered_questions_count(self, obj):
        return obj.questions.filter(answered=True).count()

    def get_youtube_id(self, obj):
        try:
            return obj.latest_video().video_id
        except Video.DoesNotExist:
            return None
