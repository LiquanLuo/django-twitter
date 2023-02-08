from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers, exceptions

from accounts.api.serializers import UserSerializer
from comments.models import Comment
from likes.models import Like
from tweets.models import Tweet


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Like
        fields = ('user', 'created_at',)


class LikeBaseSerializer(serializers.ModelSerializer):
    content_type = serializers.ChoiceField(choices=['tweet', 'comment'])
    object_id = serializers.IntegerField()

    class Meta:
        model = Like
        fields = ('content_type', 'object_id',)

    def _get_model(self, model):
        if model == 'tweet':
            return Tweet
        if model == 'comment':
            return Comment
        return None

    def validate(self, data):
        model = self._get_model(data['content_type'])
        if not model:
            raise exceptions.ValidationError({
                'content_type': 'There is no such type.'
            })
        if not model.objects.filter(id=data['object_id']).exists():
            raise exceptions.ValidationError({
                'object_id': 'The object does not exist.'
            })
        return data


class LikeCreateSerializer(LikeBaseSerializer):
    def create(self, validated_data):
        model = self._get_model(validated_data['content_type'])
        like, _ = Like.objects.get_or_create(
            user = self.context['request'].user,
            content_type = ContentType.objects.get_for_model(model),
            object_id = validated_data['object_id']
        )
        return like

class LikeCancelSerializer(LikeBaseSerializer):
    def cancel(self):
        model = self._get_model(self.validated_data['content_type'])
        Like.objects.filter(
            user=self.context['request'].user,
            content_type=ContentType.objects.get_for_model(model),
            object_id=self.validated_data['object_id']
        ).delete()