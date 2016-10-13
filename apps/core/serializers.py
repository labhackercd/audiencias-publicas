from rest_framework import serializers
from apps.core.models import Agenda, Message, Question, Video, UpDownVote


class VoteSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField('get_content_type_name')

    def get_content_type_name(self, obj):
        return obj.content_type.name

    class Meta:
        model = UpDownVote
        fields = ('id', 'user', 'content_type', 'vote', 'object_pk')


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
